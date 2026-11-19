# SLK V22｜2025年 *Mercurialis* の真正親子・繁殖データへ進む

**2026-11-19｜2025 New Phytologist（DOI 10.1111/nph.70356）の真正Zenodo公開ZIPの取得に成功し、次段の実データ記述監査を実装。Draft PR #121限定。**

## 今回確定した真正データ

- Zenodo概念DOI [10.5281/zenodo.14542260](https://doi.org/10.5281/zenodo.14542260) は、公開版 [10.5281/zenodo.15644955](https://doi.org/10.5281/zenodo.15644955) へ解決された。概念レコードID14542260、実版ID15644955をAPIメタデータで同時確認。
- 原アーカイブ `Geito_NewPhyto_v2.zip`：**5,498,730 bytes**、Zenodo公開MD5 `ea198a76d60cdf412638c77e6e0e3d80` と実際にダウンロードしたZIPのMD5が一致。GitHub Actions [source run 44456232591](https://github.com/zuizui0223/slk/actions/runs/44456232591) のログと保存artifactで検証。
- ZIP内の原CSVは `3G.csv`（ヘッダ以外181行）、`3G_ID01.csv`（362行）、`Genotype_3P.csv`（1132行）。前二者には個体ID・Population・雄花数・雌花数・自殖率・雄性／雌性／合計繁殖成果・`Inbreeding`列があり、最後には親子遺伝子型とSSR座位列がある。さらに原著の `Fitness.R`、`Selfing.R`、`Trade-off.R`、README、RDataが同梱。**CSVの行数は独立個体数ではない**。とくに`3G_ID01.csv`の362行は複数の近交弱勢仮定を含む可能性があり、検証せず362株と呼ばない。

## 新たに実装した実測データ解析の範囲

`analysis/audit_zenodo_mercu_realized_fitness_v22.py` は、APIで概念DOIを検証→原ZIPを再取得→MD5一致を確認→ZIP内の3CSVだけを読み込み、**個体ID×集団の重複・対応数、性配分・自殖率の分布、`Inbreeding`シナリオ別の母性・父性・合計成果の記述平均**を計算する。Rコードは実行せず、元データZIPをGitHubへ再配布しない。テストと専用CIで、`Inbreeding`別の行を独立個体と誤認しないことを保証する。

この解析は**母性・父性の個票を使うが、まだ新しい選択勾配や因果的な適応度順位反転を推定するものではない**。父性推定の再計算にはSSRと原著コードのID結合規則の別監査が必要。近交弱勢は**実測ではなくシナリオ**である。

## SLKの生物学的な問い

**相手不足時に両性機能を残す利点は、同じ個体の実現父性・母性・自殖子の生存損失を差し引いても残るか。** この原データでは、少なくとも**実測した性配分・自殖率・成熟種子・父性推定値**を同じ個体に対応させられる可能性がある。最初に独立母株数、父性・母性データの重なり、近交弱勢仮定別の合計成果を監査し、その後に実測と仮定を明確に分けた条件付き適応度比較へ進む。

**ただし雄あり／なし環境の独立処理比較、自然のδ、子の実際の成体生存、分業型の長期固定はこのCSVだけでは証明されない。** 別の2024年六倍体野外実験と同一個体群として結合しない。

## 検証ステータス

- [2025 Zenodo ZIP source verification V21](https://github.com/zuizui0223/slk/actions/runs/44456232591)：**成功**、取得・MD5一致・3CSV列名と行数を確認。
- [V22 original data audit code](../analysis/audit_zenodo_mercu_realized_fitness_v22.py)、[4 unit tests](../tests/test_zenodo_mercu_realized_fitness_v22.py)、[dedicated workflow](../.github/workflows/slk-2025-realized-fitness-v22.yml)：**実行結果待ち**。CIの緑だけではなく、artifactの`state=verified_descriptive`を確認してから数値を確定する。

`main`、凍結Am Nat主稿、ANTO、Island、aza3は変更しない。PR #121はDraftのまま。
