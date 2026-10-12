# GitHub Upload Guide — Sinhala / English

## Method A — GitHub website එකෙන් (beginner friendly)

1. [github.com](https://github.com) login කරන්න.
2. Top-right **+ → New repository** click කරන්න.
3. Repository name: `IoMT-Risk-Prediction-Dataset` (suggested). Short description දාන්න.
4. **Private** select කරන්න until source-data licensing and contributor approval are confirmed. Public කරන්න පුළුවන් ඒවා තහවුරු කරගත්තට පස්සේ.
5. **Add a README** checkbox off තියාගෙන **Create repository** click කරන්න (package එකේ README දැනටමත් තියෙනවා).
6. ZIP එක locally extract කරලා `IoMT_Risk_Dataset_GitHub` folder එක open කරන්න.
7. New repository page → **uploading an existing file** හෝ **Add file → Upload files**.
8. Folder එක ඇතුළේ තියෙන `README.md`, `data`, `docs`, `scripts`, `.gitignore`, `requirements.txt`, `CITATION.md`, `LICENSE_GUIDANCE.md` files/folders **select කරලා drag-and-drop** කරන්න. ZIP file එකම repository එකට දාන්න එපා; extracted files upload කරන්න.
9. Preview file list එකේ `data/...csv` සහ Markdown docs තියෙනවාද බලන්න. **Commit changes** click කරන්න.
10. Repository page එකේ README auto-render වෙනවා. `docs/VALIDATION_REPORT.md` සහ `docs/FEATURE_DESCRIPTIONS.md` open කරලා test කරන්න.

**Note:** GitHub browser uploader individual files සඳහා 25 MiB limit යෙදෙන්න පුළුවන්; මෙම CSV එක ~7.5 MB නිසා සාමාන්‍යයෙන් ඒ limit එකට අඩුයි. Git command line GitHub සාමාන්‍යව 100 MiBට වැඩි files block කරයි; මේ dataset එකට Git LFS අවශ්‍ය නැහැ.

## Method B — Git Bash / terminal

Install Git if needed: https://git-scm.com/downloads . Empty repository එක GitHub එකේ create කරන්න (README/.gitignore auto-add නොකරන්න).

```bash
cd "/path/to/IoMT_Risk_Dataset_GitHub"
git init
git branch -M main
git add .
git commit -m "Add IoMT dataset, documentation and validation checks"
git remote add origin https://github.com/YOUR_USERNAME/IoMT-Risk-Prediction-Dataset.git
git push -u origin main
```

Replace `YOUR_USERNAME`; GitHub might request sign-in through the credential manager. On Windows PowerShell, use `cd "C:\Users\YOUR_USER\Desktop\IoMT_Risk_Dataset_GitHub"` (actual extracted folder path).

## Validate locally

```bash
python -m pip install -r requirements.txt
python scripts/validate_dataset.py
```

PASS means file-level structure checks passed; not that LSTM prediction accuracy or future label validity was proven.

## Before making the repo public

- [ ] Original source licenses and public-sharing rights verified
- [ ] Dataset author / group member approval obtained
- [ ] Provenance template filled using your actual Colab generator and original input sources
- [ ] All metadata / labels are described without claiming unmeasured results
- [ ] No private paths, patient records, secrets or API keys in the repo
- [ ] README and documentation reviewed by the research group

## Later updates

```bash
git add .
git commit -m "Update dataset documentation"
git push
```
