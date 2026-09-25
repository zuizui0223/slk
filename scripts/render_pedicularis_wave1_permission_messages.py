from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INQUIRY_GENERATOR = ROOT / "scripts" / "generate_pedicularis_wave1_permission_inquiry.py"

_spec = importlib.util.spec_from_file_location("ped_wave1_inquiry_generator", INQUIRY_GENERATOR)
inquiry = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(inquiry)

ACTIVITY_CN = {
    "A": "仅观察植物及其生境，不触碰或采集材料",
    "B": "拍摄植株、叶轮生特征、叶柄/苞片基部及花部形态照片",
    "C": "非破坏性测量与自然史观察（包括访花、早期虫害/产卵迹象、水分状态等）",
    "D": "采集少量凭证标本（voucher specimen）",
    "E": "采集少量叶片或组织用于后续实验/遗传分析",
    "F": "采集少量种子或果实",
}

ACTIVITY_EN = {
    "A": "visual observation only, without touching or collecting plant material",
    "B": "photography of whole plants and diagnostic morphology",
    "C": "non-destructive measurements and natural-history observations",
    "D": "collection of a small voucher specimen",
    "E": "collection of a small amount of leaf/tissue material",
    "F": "collection of a small amount of seed/fruit material",
}


def _channel_hint(public_contact: str) -> str:
    has_email = "@" in public_contact
    has_digit = any(ch.isdigit() for ch in public_contact)
    if has_email and has_digit:
        return "EMAIL_OR_PHONE"
    if has_email:
        return "EMAIL"
    return "PHONE_OR_OFFICE"


def _locator_text(locator: dict | None) -> tuple[str, str]:
    if locator is None:
        return (
            "目前仅有历史候选地点信息，尚无可公开核实的精确定位；拟在获得管理方指引后进行现场确认。",
            "Only a historical candidate locality is currently registered; no exact public locator is claimed.",
        )
    if locator["locator_type"] == "POINT":
        p = locator["point"]
        return (
            f"历史/公开资料中的调查定位约为 {p['latitude_deg']:.6f}°N, {p['longitude_deg']:.6f}°E；该坐标仅用于寻找历史地点，不能视为现生种群坐标。",
            f"The registered scouting point is approximately {p['latitude_deg']:.6f}°N, {p['longitude_deg']:.6f}°E; it is a scouting locator only, not a current population coordinate.",
        )
    e = locator["envelope"]
    return (
        (
            "公开资料仅支持一个调查范围："
            f"{e['lat_min_deg']:.6f}–{e['lat_max_deg']:.6f}°N, "
            f"{e['lon_min_deg']:.6f}–{e['lon_max_deg']:.6f}°E；"
            "该范围不是具体植株位置。"
        ),
        (
            "The public source supports only a scouting envelope: "
            f"{e['lat_min_deg']:.6f}–{e['lat_max_deg']:.6f}°N, "
            f"{e['lon_min_deg']:.6f}–{e['lon_max_deg']:.6f}°E; "
            "this is not an individual-plant locality."
        ),
    )


def _activity_questions_cn() -> str:
    lines = []
    for activity_id in "ABCDEF":
        lines.append(
            f"{activity_id}. {ACTIVITY_CN[activity_id]}："
            "请分别说明【允许 / 无需另行许可 / 禁止 / 尚无法确认】，"
            "并注明该项决定的有效起止日期、适用条件及书面依据。"
        )
    return "\n".join(lines)


def _activity_questions_en() -> str:
    lines = []
    for activity_id in "ABCDEF":
        lines.append(
            f"{activity_id}. {ACTIVITY_EN[activity_id]}: "
            "please state separately whether this is ALLOWED, NO PERMISSION REQUIRED, "
            "PROHIBITED, or UNRESOLVED, and provide activity-specific validity dates, "
            "conditions, and a written reference."
        )
    return "\n".join(lines)


def render(candidate_id: str) -> dict:
    packet = inquiry.build(candidate_id)
    locator_cn, locator_en = _locator_text(packet["scouting_locator_snapshot"])
    candidate = packet["candidate"]

    messages = []
    for route in packet["contact_routes"]:
        route_question = route["question_to_resolve"]
        subject_cn = (
            "关于 Pedicularis rex（马先蒿属）现生种群确认及科研活动许可路径的咨询"
        )
        subject_en = (
            "Inquiry on permission routing for fresh Pedicularis rex population verification"
        )
        body_cn = f"""尊敬的{route['organization']}：

您好。我们正在开展一项关于 Pedicularis rex 的生态学研究前期确认工作。当前阶段的目的，是在既有文献/公开记录所指示的候选地点，确认本季是否仍存在可识别的开花种群，并在任何后续野外活动前明确正确的管理与许可程序。

候选地点：{candidate['region_or_site']}
候选编号：{candidate['candidate_id']}
{locator_cn}

本次咨询本身不代表我们已获得任何采集或研究许可，也不会把公共开放、旅游访问或历史记录视为科研许可。

针对贵单位所对应的管理/监管路径，我们希望首先确认：
{route_question}

同时，为避免把一种活动的许可误用于另一种活动，请对以下 A–F 六类活动分别答复：

{_activity_questions_cn()}

如贵单位并非其中某项活动的正确审批/管理主体，也恳请告知应联系的具体单位或部门。

对于每一项可允许或无需另行许可的活动，我们希望获得：
1. 明确的书面回复或许可/备案编号；
2. 该活动的有效起止日期；
3. 适用的地点范围；
4. 必须遵守的现场条件；
5. 是否还需另行取得场地管理方、林草/野生植物主管部门或其他机构的批准。

申请人姓名：REQUIRED_BEFORE_SEND
所属机构：REQUIRED_BEFORE_SEND
联系邮箱：REQUIRED_BEFORE_SEND

感谢您的指导。"""

        body_en = f"""Dear {route['organization']},

We are preparing a prospective ecological study involving Pedicularis rex. At this stage, our goal is only to verify whether a recognizable flowering population is currently present at a candidate locality identified from prior literature or public records, and to identify the correct management and permission pathway before any further field activity.

Candidate locality: {candidate['region_or_site']}
Candidate ID: {candidate['candidate_id']}
{locator_en}

This inquiry does not assume that any research or collecting permission has already been granted.

Route-specific question:
{route_question}

Please address activities A-F separately:

{_activity_questions_en()}

For each activity that is allowed or requires no additional permission, please provide a written reference, activity-specific validity dates, spatial scope, conditions, and any additional authority/site approvals that are required.

Requester name: REQUIRED_BEFORE_SEND
Institution: REQUIRED_BEFORE_SEND
Email: REQUIRED_BEFORE_SEND

Thank you for your guidance."""

        messages.append(
            {
                "route_id": route["route_id"],
                "route_type": route["route_type"],
                "organization": route["organization"],
                "public_contact": route["public_contact"],
                "channel_hint": _channel_hint(route["public_contact"]),
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
        )

    return {
        "schema_version": "SLK_PEDICULARIS_WAVE1_PERMISSION_MESSAGE_DRAFTS_V1",
        "status": "DRAFT_NOT_SENT",
        "candidate": candidate,
        "scouting_locator_snapshot": packet["scouting_locator_snapshot"],
        "messages": messages,
        "claim_ceiling": (
            "MESSAGE_DRAFTS_ONLY_NO_CONTACT_EXECUTED_NO_PERMISSION_GRANTED_"
            "NO_FRESH_CONTEXT_NO_P0_SIGNAL"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Render unsent Chinese/English WAVE1 permission inquiry message drafts"
    )
    parser.add_argument("--candidate-id", required=True)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    result = render(args.candidate_id)
    args.output.write_text(
        json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
