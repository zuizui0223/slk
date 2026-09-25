from __future__ import annotations

import argparse
import csv
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLANNER_PATH = ROOT / "scripts" / "plan_pedicularis_wave1_permission_followups.py"
RENDER_PATH = ROOT / "scripts" / "render_pedicularis_wave1_permission_messages.py"

_spec_plan = importlib.util.spec_from_file_location("ped_followup_planner", PLANNER_PATH)
planner = importlib.util.module_from_spec(_spec_plan)
assert _spec_plan.loader is not None
_spec_plan.loader.exec_module(planner)

_spec_render = importlib.util.spec_from_file_location("ped_initial_renderer", RENDER_PATH)
initial_renderer = importlib.util.module_from_spec(_spec_render)
assert _spec_render.loader is not None
_spec_render.loader.exec_module(initial_renderer)


def _read(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def render_followup(
    rows: list[dict[str, str]],
    policy_payload: dict,
    *,
    route_id: str,
    as_of_date: str,
) -> dict:
    plan = planner.plan(
        rows,
        policy_payload,
        as_of_date=as_of_date,
    )
    matches = [r for r in plan["routes"] if r["route_id"] == route_id]
    if len(matches) != 1:
        raise ValueError(f"follow-up route not uniquely planned: {route_id}")
    route_plan = matches[0]
    if route_plan["action"] != "FOLLOWUP_DUE":
        raise ValueError(
            f"follow-up route is not due: {route_id}/{route_plan['action']}"
        )

    ledger_row = next(
        row for row in rows if row["route_id"].strip() == route_id
    )
    candidate_id = ledger_row["candidate_id"].strip()
    initial = initial_renderer.render(candidate_id)
    message = next(
        m for m in initial["messages"] if m["route_id"] == route_id
    )
    n = route_plan["followup_number"]
    previous_date = (
        ledger_row["last_followup_date"].strip()
        if int(ledger_row["followup_attempts_completed"]) > 0
        else ledger_row["outreach_date"].strip()
    )
    previous_reference = (
        ledger_row["last_followup_reference"].strip()
        if int(ledger_row["followup_attempts_completed"]) > 0
        else ledger_row["outreach_reference"].strip()
    )

    subject_cn = f"关于此前 Pedicularis rex 科研许可咨询的第{n}次跟进"
    subject_en = f"Follow-up {n}: Pedicularis rex permission inquiry"

    body_cn = f"""尊敬的{message['organization']}：

您好。我们于 {previous_date} 就 Pedicularis rex 现生种群确认及科研活动许可路径向贵单位发送过咨询（记录编号：{previous_reference}）。截至本次prospective follow-up计划的执行日期，我们的跟踪记录中尚未收到该route的实质性答复，因此按照预先冻结的跟进时间表进行第 {n} 次跟进。

本次跟进不改变原咨询的活动范围，也不把未回复解释为允许或拒绝。我们仍希望贵单位对 A–F 六类活动分别说明【允许 / 无需另行许可 / 禁止 / 尚无法确认】，并分别提供书面依据、有效起止日期、适用地点范围和条件。

{initial_renderer._activity_questions_cn()}

如贵单位并非某项活动的正确管理或审批主体，烦请告知应联系的正式单位或部门。

申请人姓名：REQUIRED_BEFORE_SEND
所属机构：REQUIRED_BEFORE_SEND
联系邮箱：REQUIRED_BEFORE_SEND

感谢您的指导。"""

    body_en = f"""Dear {message['organization']},

We previously contacted your organization on {previous_date} regarding the permission pathway for fresh Pedicularis rex population verification (tracking reference: {previous_reference}). Our registered outreach record contains no substantive response for this route as of the date on which this prospectively scheduled follow-up is being executed, so this is follow-up number {n} under the frozen follow-up policy.

This follow-up does not change the scope of the original inquiry, and silence is not interpreted as permission or refusal. Please continue to address activities A-F separately and provide written references, activity-specific validity dates, spatial scope, and conditions.

{initial_renderer._activity_questions_en()}

If your organization is not the correct authority or site manager for an activity, please identify the appropriate formal contact.

Requester name: REQUIRED_BEFORE_SEND
Institution: REQUIRED_BEFORE_SEND
Email: REQUIRED_BEFORE_SEND

Thank you for your guidance."""

    followup_message = {
        "route_id": message["route_id"],
        "route_type": message["route_type"],
        "organization": message["organization"],
        "public_contact": message["public_contact"],
        "channel_hint": message["channel_hint"],
        "message_kind": "FOLLOWUP",
        "followup_number": n,
        "policy_due_date": route_plan["due_date"],
        "prior_contact_date": previous_date,
        "prior_contact_reference": previous_reference,
        "status": "DRAFT_NOT_SENT",
        "subject_cn": subject_cn,
        "body_cn": body_cn,
        "subject_en": subject_en,
        "body_en": body_en,
        "send_guard": {
            "requester_identity_filled": False,
            "institution_filled": False,
            "reply_contact_filled": False,
            "human_review_required": True,
            "automatic_send_allowed": False,
        },
    }

    return {
        "schema_version": "SLK_PEDICULARIS_WAVE1_PERMISSION_MESSAGE_DRAFTS_V1",
        "status": "DRAFT_NOT_SENT",
        "candidate": initial["candidate"],
        "scouting_locator_snapshot": initial["scouting_locator_snapshot"],
        "message_kind": "FOLLOWUP",
        "followup_policy_freeze_commit": plan["policy_freeze_commit"],
        "followup_as_of_date": plan["as_of_date"],
        "messages": [followup_message],
        "claim_ceiling": (
            "FOLLOWUP_MESSAGE_DRAFT_ONLY_NO_CONTACT_EXECUTED_"
            "NO_RESPONSE_NO_PERMISSION_NO_FRESH_CONTEXT"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Render a due WAVE1 permission follow-up message draft"
    )
    parser.add_argument("outreach_ledger_csv", type=Path)
    parser.add_argument("followup_policy_json", type=Path)
    parser.add_argument("--route-id", required=True)
    parser.add_argument("--as-of-date", required=True)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    result = render_followup(
        _read(args.outreach_ledger_csv),
        json.loads(args.followup_policy_json.read_text(encoding="utf-8")),
        route_id=args.route_id,
        as_of_date=args.as_of_date,
    )
    args.output.write_text(
        json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
