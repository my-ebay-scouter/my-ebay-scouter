# MY eBay SCOUTER 3.0 starter

- Daily GitHub Actions scan at 08:00 JST.
- Uses eBay Marketing API BEST_SELLING by verified category ID.
- Writes data/daily_report.json and creates search links for Mercari, Yahoo!フリマ, Yahoo!オークション.
- No scraping of domestic marketplaces; no bypassing access controls.

## Setup
1. Obtain eBay production Client ID and Client Secret.
2. Confirm your application has production access to eBay Buy/Marketing APIs. Production access is restricted and may require approval.
3. GitHub repository Settings → Secrets and variables → Actions: add `EBAY_CLIENT_ID` and `EBAY_CLIENT_SECRET`.
4. Fill verified `ebay_category_id` values in config.json. Do not guess IDs; use eBay Taxonomy/category browser.
5. Upload this package's files/folders into the existing repository, preserving `.github/workflows/`.
6. GitHub Actions → MY eBay SCOUTER daily scan → Run workflow to test.

## Limits
Marketing API BEST_SELLING is a popularity signal, not sold-through history. Marketplace Insights sales history is limited release. Domestic marketplace listing extraction is not implemented; only search links are generated. Profit cannot be confirmed until domestic asking price, condition, shipping and actual fee settings are checked.

Settings: budget ¥30,000; target profit ¥5,000; watches, cameras/optics, audio, telescopes; daily at 08:00 JST.
