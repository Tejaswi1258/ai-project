# Vercel Deployment Instructions

## Deploy to Vercel

1. Install Vercel CLI:
```bash
npm install -g vercel
```

2. Login to Vercel:
```bash
vercel login
```

3. Deploy the project:
```bash
cd c:\ai-project\sentiment-ai
vercel
```

4. Follow the prompts:
   - Set up and deploy? Yes
   - Which scope? Select your account
   - Link to existing project? No
   - Project name? ai-project (or your preferred name)
   - Directory? ./
   - Override settings? No

5. For production deployment:
```bash
vercel --prod
```

## Alternative: Deploy via Vercel Dashboard

1. Go to https://vercel.com/
2. Click "Add New Project"
3. Import your GitHub repository: https://github.com/Tejaswi1258/ai-project
4. Vercel will auto-detect the configuration
5. Click "Deploy"

Your app will be live at: https://your-project-name.vercel.app
