# Michelin Guide Singapore: Data Analysis Project

<div align="center">
  <img src="https://upload.wikimedia.org/wikipedia/commons/9/9f/Michelin_guide_logo.png" alt="Michelin Guide Logo" width="300"/>
  
  <p><em>Does Michelin Recognition in Singapore Accurately Reflect Dining Quality?</em></p>
  
  <p>A comprehensive data-driven investigation examining whether Michelin stars truly guarantee superior dining experiences by analyzing customer sentiment, food safety, and value for money.</p>
</div>

---

## 📊 Project Overview

This website showcases a Tableau dashboard project that analyzes Michelin-recognized restaurants in Singapore through multiple lenses:

- **Customer Experience** - Sentiment analysis from Google Maps and TripAdvisor reviews
- **Food Safety** - Singapore Food Agency (SFA) hygiene grading data
- **Value Assessment** - Price-to-quality ratio and affordability analysis
- **Hidden Gems** - Discovery of non-Michelin alternatives with exceptional quality

The project challenges the assumption that Michelin recognition is the ultimate dining quality indicator and provides data-driven insights to help diners make informed decisions.

---

## ✨ Features

### 🏠 Introduction Page
- Project proposal and research questions
- Methodology overview
- Interactive problem statement with key statistics
- Michelin Guide-inspired elegant design

### 📈 Dashboards Page
- Placeholder sections for Tableau visualizations
- Ready for embedding Tableau Public dashboards
- Organized by analysis category

### 📖 Insights & Story
- Narrative-driven data storytelling
- Five key research questions explored:
  1. Are Michelin restaurants actually better?
  2. Is the price justified?
  3. Are there better non-Michelin alternatives?
  4. Does safety align with quality?
  5. Where should you actually dine?
- Data source citations with direct links

---

## 🎨 Design Philosophy

The website features a **sophisticated, classy editorial layout** inspired by the official Michelin Guide Paris website:

- **Color Palette**: Michelin red (#C8102E) and gold (#F4C100) as subtle accents
- **Typography**: Official Figtree font family for refined readability
- **Layout**: Clean minimalist design with generous whitespace
- **Components**: Professional content blocks and decorative dividers
- **Icons**: Lucide React icons for a modern, professional appearance

---

## 🛠️ Technologies Used

### Frontend Framework
- **React 18.3.1** - Modern UI library
- **React Router 7.13.0** - Client-side routing
- **TypeScript** - Type-safe development

### Styling
- **Tailwind CSS 4.1.12** - Utility-first CSS framework
- **Custom CSS** - Theme tokens and font imports

### UI Components & Icons
- **Lucide React 0.487.0** - Professional icon library
- **Motion 12.23.24** - Animation library
- **Radix UI** - Accessible component primitives

### Build Tools
- **Vite 6.3.5** - Fast development and build tool
- **pnpm** - Efficient package manager

---

## 📁 Project Structure

```
/
├── src/
│   ├── app/
│   │   ├── components/
│   │   │   ├── figma/
│   │   │   │   └── ImageWithFallback.tsx
│   │   │   ├── Navigation.tsx
│   │   │   └── StarIcon.tsx
│   │   ├── pages/
│   │   │   ├── Home.tsx
│   │   │   ├── Dashboards.tsx
│   │   │   └── Insights.tsx
│   │   ├── App.tsx
│   │   └── routes.ts
│   ├── imports/
│   │   └── [Figma assets]
│   ├── styles/
│   │   ├── fonts.css
│   │   ├── index.css
│   │   └── theme.css
│   └── main.tsx
├── index.html
├── package.json
├── vite.config.ts
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites
- **Node.js** (v18 or higher)
- **pnpm** (recommended) or npm

### Installation

1. **Clone the repository**
   ```bash
   git clone <https://github.com/swen-teo/singapore-michelin-data>
   cd singapore-michelin-data/website
   ```

2. **Install dependencies**
   ```bash
   pnpm install
   # or
   npm install
   ```

3. **Start development server**
   ```bash
   pnpm dev
   # or
   npm run dev
   ```

4. **Open in browser**
   ```
   http://localhost:5173
   ```

### Build for Production

```bash
pnpm build
# or
npm run build
```

The build output will be in the `dist/` directory.

---

## 📊 Data Sources

This project integrates data from the following sources:

### 1. **Kaggle - Michelin Guide Restaurants (2021)**
- **URL**: https://www.kaggle.com/datasets/ngshiheng/michelin-guide-restaurants-2021
- **Contains**: Restaurant details, cuisine types, and award information
- **Usage**: Primary dataset for Michelin-recognized establishments

### 2. **Apify - Restaurant Review Aggregator**
- **URL**: https://apify.com/tri_angle/restaurant-review-aggregator/api/javascript
- **Contains**: Customer reviews from Google Maps and TripAdvisor
- **Usage**: Sentiment analysis and customer experience data

### 3. **Data.gov.sg - Certificate Grading Info**
- **URL**: https://data.gov.sg/datasets/d_546a95c5e6a0a264a82247ec107a0629/view
- **Contains**: Licensed eating establishments hygiene grading (GeoJSON)
- **Usage**: SAFE framework food safety data

### 4. **Singstat - Household Expenditure Survey**
- **URL**: https://www.singstat.gov.sg/find-data/search-by-theme/households/household-expenditure/visualising-data/household-expenditure-survey-dashboard
- **Contains**: Household spending patterns in Singapore
- **Usage**: Affordability and value analysis context

---

## 🎯 Key Research Questions

### 1. Are Michelin restaurants actually better?
- Rating distribution analysis
- Sentiment scoring across award tiers
- Award distribution patterns

### 2. Is the price justified?
- Value score calculation (rating ÷ price)
- Price vs. sentiment correlation
- Affordability benchmarking

### 3. Are there better alternatives?
- Hidden gem identification
- Geographic clustering analysis
- Cuisine type performance

### 4. Does safety align with quality?
- Hygiene grade vs. Michelin tier cross-tabulation
- Safety vs. price correlation
- Sentiment vs. safety alignment

### 5. Where should you actually dine?
- Multi-criteria recommendation system
- Personalized filtering by priorities
- Decision framework for different diner types

---

## 🎨 Customization

### Updating Colors
Edit the color values in `/src/styles/theme.css`:
```css
--color-michelin-red: #C8102E;
--color-michelin-gold: #F4C100;
```

### Changing Typography
Update font imports in `/src/styles/fonts.css` and theme tokens in `/src/styles/theme.css`.

### Adding New Pages
1. Create a new component in `/src/app/pages/`
2. Add route in `/src/app/routes.ts`
3. Update navigation in `/src/app/components/Navigation.tsx`

---

## 📱 Responsive Design

The website is fully responsive and optimized for:
- **Desktop** (1920px+)
- **Laptop** (1024px - 1919px)
- **Tablet** (768px - 1023px)
- **Mobile** (320px - 767px)

---

## 🚀 Deployment

### Deploy to Netlify
1. Connect your repository to Netlify
2. Build command: `pnpm build` or `npm run build`
3. Publish directory: `dist`

### Deploy to Vercel
1. Import your repository
2. Framework preset: Vite
3. Build command: `pnpm build` or `npm run build`
4. Output directory: `dist`

### Deploy to GitHub Pages
1. Install `gh-pages`: `pnpm add -D gh-pages`
2. Update `vite.config.ts` with base path
3. Add deploy script to `package.json`:
   ```json
   "deploy": "pnpm build && gh-pages -d dist"
   ```
4. Run: `pnpm deploy`

---

## 📄 License

This project is created for educational and research purposes. The Michelin Guide name and logo are trademarks of Michelin. This project is not affiliated with or endorsed by Michelin.

---

## 👤 Author

**Your Name**
- Project: Michelin Singapore Dining Quality Analysis
- Academic Institution: [Your University/Institution]
- Course: [Your Course Name]

---

## 🙏 Acknowledgments

- **Michelin Guide** - For inspiring this analysis
- **Singapore Food Agency** - For food safety transparency
- **Singapore Department of Statistics** - For household expenditure data
- **Data Contributors** - All open data providers listed in Data Sources

---

## 📧 Contact

For questions or feedback about this project:
- **Email**: your.email@example.com
- **LinkedIn**: [Your LinkedIn Profile]
- **GitHub**: [Your GitHub Profile]

---

<div align="center">
  <p><strong>Stars may guide you, but data empowers you.</strong></p>
  <p><em>Make informed dining decisions with data-driven insights.</em></p>
</div>
