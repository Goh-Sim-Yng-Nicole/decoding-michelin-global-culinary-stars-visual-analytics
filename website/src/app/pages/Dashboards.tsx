import { TableauEmbed } from "../components/TableauEmbed";

export function Dashboards() {
  const dashboards = [
    {
      id: 1,
      title: "Overall (The Prestige Landscape)",
      description: "Establishing the baseline of Singapore's Michelin scene. This dashboard explores who receives these prestigious awards, the types of cuisines they serve, their locations across the island, and the heavy preference for fine dining over street food.",
      embedUrl: "https://public.tableau.com/views/En-tire-lyOverrated/TheMichelinLandscapeinSingapore",
      height: "1000px",
      type: "tableau"
    },
    {
      id: 2,
      title: "What Diners Actually Say",
      description: "Before diving into sentiment scores, hear it straight from diners. Select any restaurant (or view all restaurants) to see the words that appear most often in their Google reviews.",
      embedUrl: "/wordcloud.html",
      height: "680px",
      type: "local"
    },
    {
      id: 3,
      title: "Taste and Service",
      description: "Investigating whether Michelin-recognized restaurants actually deliver a superior culinary and hospitality experience. This dashboard analyzes customer sentiment to reveal who truly excels at food and service, and whether the most favored cuisines taste the best to everyday diners.",
      embedUrl: "https://public.tableau.com/views/En-tire-lyOverrated/TasteandServiceInsights",
      height: "1000px",
      type: "tableau"
    },
    {
      id: 4,
      title: "Price and Value",
      description: "Deconstructing the financial reality of fine dining. This dashboard examines whether high prices are truly justified, helping diners identify overpriced tourist traps and discover hidden gems that offer the best value for their money.",
      embedUrl: "https://public.tableau.com/views/En-tire-lyOverrated/AffordabilityandValue",
      height: "1000px",
      type: "tableau"
    },
    {
      id: 5,
      title: "Hygiene (The Safety Blind Spot)",
      description: "Stripping away the glamour to examine basic food safety. This dashboard tests the assumption that expensive restaurants are inherently safer, revealing the true hygiene standards across different Michelin award tiers and serving as a guide to the riskiest dining categories.",
      embedUrl: "https://public.tableau.com/views/En-tire-lyOverrated/FoodSafetyandHygieneAnalysis",
      height: "1000px",
      type: "tableau"
    },
    {
      id: 6,
      title: "Smart Diner Recommender",
      description: "An actionable tool designed to empower diners in finding safe, high-value dining alternatives. By allowing users to prioritize their own preferences across taste, value, service, and hygiene, this dashboard provides personalized restaurant recommendations that look beyond pure prestige. Note: Due to Tableau embedding limitations, restaurant links directing to Google Maps may not open when clicked.",
      embedUrl: "https://public.tableau.com/views/En-tire-lyOverrated/SmartRecommender",
      height: "1000px",
      type: "tableau"
    }
  ];

  return (
    <div className="min-h-screen bg-white">
      {/* Header Section */}
      <div className="border-b border-gray-200 bg-[#F9F8F6]">
        <div className="max-w-7xl mx-auto px-4 sm:px-8 py-10 sm:py-16">
          <div className="text-center max-w-3xl mx-auto">
            <div className="inline-block mb-4 sm:mb-6">
              <div className="flex items-center gap-2 text-xs sm:text-sm text-gray-500 uppercase tracking-widest">
                <div className="w-8 sm:w-12 h-px bg-gray-300"></div>
                <span>Data Visualizations</span>
                <div className="w-8 sm:w-12 h-px bg-gray-300"></div>
              </div>
            </div>
            <h1 className="text-3xl sm:text-4xl md:text-5xl font-bold mb-4 sm:mb-6 text-[#2B2B2B]">
              Interactive Dashboards
            </h1>
            <p className="text-base sm:text-lg md:text-xl text-gray-600 leading-relaxed font-light">
              Explore our comprehensive data visualizations that transform raw data into
              actionable insights about Singapore's Michelin dining scene.
            </p>
          </div>
        </div>
      </div>

      {/* Dashboards Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-8 py-10 sm:py-16">
        <div className="space-y-12 sm:space-y-20">
          {dashboards.map((dashboard) => (
            <div key={dashboard.id} className="border-b border-gray-200 pb-12 sm:pb-20 last:border-0">
              <div className="mb-6 sm:mb-8">
                <div className="flex flex-col sm:flex-row items-start gap-4 sm:gap-6 mb-4 sm:mb-6">
                  <div className="flex-shrink-0">
                    <div className="w-12 h-12 sm:w-16 sm:h-16 bg-[#C8102E] text-white flex items-center justify-center text-xl sm:text-2xl font-bold">
                      {dashboard.id}
                    </div>
                  </div>
                  <div className="flex-1">
                    <h2 className="text-2xl sm:text-3xl font-bold text-[#2B2B2B] mb-2 sm:mb-3">{dashboard.title}</h2>
                    <p className="text-gray-600 text-sm sm:text-lg leading-relaxed">{dashboard.description}</p>
                  </div>
                </div>
              </div>

              {/* Dashboard Embed */}
              <div className="w-full bg-gray-50 rounded-lg overflow-hidden shadow-sm">
                {dashboard.type === 'local' ? (
                  <iframe
                    src={dashboard.embedUrl}
                    width="100%"
                    height={dashboard.height}
                    title={dashboard.title}
                    style={{ border: 'none', display: 'block' }}
                    allowFullScreen
                  />
                ) : (
                  <>
                    <div className="overflow-x-auto">
                      <div
                        style={{ minHeight: dashboard.height, minWidth: '800px' }}
                        className="w-full"
                      >
                        <TableauEmbed 
                          src={dashboard.embedUrl}
                          height={dashboard.height}
                          title={dashboard.title}
                        />
                      </div>
                    </div>
                    <div className="md:hidden py-3 px-4 bg-gray-100 text-xs text-gray-500 text-center">
                      ← Scroll horizontally to view full dashboard →
                    </div>
                  </>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}