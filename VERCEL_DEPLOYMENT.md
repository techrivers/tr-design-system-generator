# Deploying to Vercel

This guide will help you deploy the Design System Generator to Vercel.

## Prerequisites

1. A Vercel account (sign up at [vercel.com](https://vercel.com))
2. Vercel CLI installed: `npm i -g vercel`
3. Your project ready for deployment

## Important Notes

### Serverless Limitations

- **Read-only filesystem**: The `/generated` directory won't be writable in Vercel's serverless environment. File saving is automatically disabled.
- **Function timeout**: Default is 10 seconds for Hobby plan, 60 seconds for Pro. The `vercel.json` is configured for 60 seconds.
- **Cold starts**: First request may be slower due to serverless cold starts.

### Environment Variables

If you're using API keys (e.g., for LiteLLM), set them in Vercel:

1. Go to your project settings in Vercel dashboard
2. Navigate to "Environment Variables"
3. Add your variables (e.g., `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, etc.)

## Deployment Steps

### Option 1: Deploy via Vercel CLI

1. **Install Vercel CLI** (if not already installed):
   ```bash
   npm i -g vercel
   ```

2. **Login to Vercel**:
   ```bash
   vercel login
   ```

3. **Deploy**:
   ```bash
   vercel
   ```

4. **For production deployment**:
   ```bash
   vercel --prod
   ```

### Option 2: Deploy via GitHub Integration

1. **Push your code to GitHub** (if not already):
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

2. **Import project in Vercel**:
   - Go to [vercel.com/new](https://vercel.com/new)
   - Import your GitHub repository
   - Vercel will auto-detect the Python project
   - Configure environment variables if needed
   - Click "Deploy"

## Project Structure for Vercel

```
design-system-agent/
├── api/
│   └── index.py          # Vercel serverless function entry point
├── web/
│   ├── app.py            # FastAPI application
│   ├── static/           # Static files (CSS, JS, etc.)
│   └── templates/        # Jinja2 templates
├── vercel.json           # Vercel configuration
├── requirements.txt      # Python dependencies
└── .vercelignore        # Files to exclude from deployment
```

## Configuration Files

### `vercel.json`
- Configures Python runtime
- Sets up routing for static files and API routes
- Sets function timeout to 60 seconds

### `api/index.py`
- Entry point for Vercel serverless functions
- Imports and exposes the FastAPI app

## Troubleshooting

### Issue: Function timeout
**Solution**: Upgrade to Vercel Pro plan for 60-second timeout, or optimize your agent processing.

### Issue: Module not found errors
**Solution**: Ensure all dependencies are in `requirements.txt` and properly installed.

### Issue: Static files not loading
**Solution**: Check that `web/static/` directory exists and files are included in deployment.

### Issue: API keys not working
**Solution**: Set environment variables in Vercel dashboard under Project Settings > Environment Variables.

## Monitoring

- Check function logs in Vercel dashboard under "Functions" tab
- Monitor performance in "Analytics" section
- Set up error tracking if needed

## Cost Considerations

- **Hobby Plan**: Free tier includes 100GB bandwidth, 100 hours of function execution
- **Pro Plan**: $20/month for more resources and longer timeouts
- Check [Vercel pricing](https://vercel.com/pricing) for current details

## Alternative: Deploy Static Frontend + Separate API

If you encounter issues with the full-stack deployment, consider:

1. Deploy the frontend (HTML/CSS/JS) as static files on Vercel
2. Deploy the FastAPI backend separately (e.g., on Railway, Render, or Fly.io)
3. Update frontend API calls to point to the separate backend URL

This approach gives you more control but requires managing two deployments.
