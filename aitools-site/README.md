# AI Tools Hub — Affiliate Website

Automated affiliate marketing website for AI tools.
Publishes one new SEO article daily using GitHub Actions + Groq AI.
Hosted FREE on GitHub Pages.

## Setup (30 minutes, one time)

### Step 1: Create GitHub repo
1. Go to github.com → New repository
2. Name it `aitools-site`
3. Set to **Public** (required for free GitHub Pages)

### Step 2: Push this code
```bash
git init
git add .
git commit -m "Initial site setup"
git remote add origin https://github.com/YOUR_USERNAME/aitools-site.git
git push -u origin main
```

### Step 3: Enable GitHub Pages
1. Go to repo → Settings → Pages
2. Source: Deploy from branch → main → / (root)
3. Click Save
4. Your site will be live at: `https://YOUR_USERNAME.github.io/aitools-site`

### Step 4: Add GROQ_API_KEY secret
1. Repo → Settings → Secrets → Actions → New secret
2. Name: `GROQ_API_KEY`
3. Value: your Groq key from console.groq.com (free)

### Step 5: Sign up for affiliate programs

Sign up for these (all free, approved instantly or within 24 hours):

| Program | URL | Commission |
|---------|-----|------------|
| Writesonic | writesonic.com/affiliates | 30% recurring |
| Canva | canva.com/affiliates | 20% per sale |
| Jasper | jasper.ai/affiliates | 25% recurring |
| Rytr | rytr.me/affiliates | 30% recurring |
| Grammarly | grammarly.com/affiliates | $0.20 per signup + more |
| GetResponse | getresponse.com/affiliates | 33-50% recurring |

### Step 6: Add your affiliate links
Open `generate_content.py` and replace `YOUR_ID` in `AFFILIATE_LINKS`
with your actual affiliate IDs from each program.

Also update `index.md` with your real affiliate links.

### Step 7: Test it
Go to Actions tab → Daily Content Publisher → Run workflow

## How it earns money

1. Someone Googles "best AI writing tools 2026"
2. Your article ranks on Google (takes 3-6 months to rank)
3. They read your article and click an affiliate link
4. They sign up for Writesonic
5. You earn 30% of their monthly subscription = $4.80-$14.70/month
6. They stay subscribed → you keep earning every month

## Realistic income timeline

- Month 1-3: Writing articles, no income yet (Google takes time to index)
- Month 4-6: First clicks, first commissions ($10-50/month)
- Month 6-12: Traffic growing, $100-500/month
- Month 12-18: Established site, $500-2000/month

## Cost: $0/month
- GitHub Pages hosting: FREE
- Groq API (article writing): FREE
- Domain (optional): $10/year for custom domain
