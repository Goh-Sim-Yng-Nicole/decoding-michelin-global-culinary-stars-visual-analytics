export function Footer() {
  return (
    <footer className="bg-[#2B2B2B] text-white py-12 mt-20">
      <div className="max-w-6xl mx-auto px-4 sm:px-8">
        <div className="grid md:grid-cols-3 gap-8">
          <div>
            <h3 className="text-xl mb-4">About This Project</h3>
            <p className="text-gray-300 text-sm leading-relaxed">
              A comprehensive data analytics project examining whether Michelin recognition in Singapore 
              accurately reflects dining quality through customer sentiment, food safety, and affordability.
              <br /><br />
              <a 
                href="https://public.tableau.com/shared/67C6MHYTP?:display_count=n&:origin=viz_share_link"
                target="_blank"
                rel="noopener noreferrer"
                className="text-[#F4C100] hover:underline inline-flex items-center gap-1.5 font-medium"
              >
                View Tableau Analysis →
              </a>
            </p>
          </div>
          
          <div>
            <h3 className="text-xl mb-4">Data Sources</h3>
            <ul className="text-gray-300 text-sm space-y-2">
              <li>
                <a 
                  href="https://www.kaggle.com/datasets/ngshiheng/michelin-guide-restaurants-2021"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="hover:text-[#F4C100] transition-colors"
                >
                  • Kaggle - Michelin Guide Restaurants
                </a>
              </li>
              <li>
                <a 
                  href="https://apify.com/tri_angle/restaurant-review-aggregator/api/javascript"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="hover:text-[#F4C100] transition-colors"
                >
                  • Apify - Restaurant Review Aggregator
                </a>
              </li>
              <li>
                <a 
                  href="https://data.gov.sg/datasets/d_546a95c5e6a0a264a82247ec107a0629/view"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="hover:text-[#F4C100] transition-colors"
                >
                  • Data.gov.sg - Certificate Grading Info
                </a>
              </li>
              <li>
                <a 
                  href="https://www.singstat.gov.sg/find-data/search-by-theme/households/household-expenditure/visualising-data/household-expenditure-survey-dashboard"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="hover:text-[#F4C100] transition-colors"
                >
                  • Singstat - Household Expenditure Survey
                </a>
              </li>
            </ul>
          </div>
          
          <div>
            <h3 className="text-xl mb-4">Group 1</h3>
            <p className="text-gray-300 text-sm leading-relaxed">
              Data Analytics & Visualization Project<br />
              Tableau Dashboard Development<br />
              March 2026
            </p>
          </div>
        </div>
        
        <div className="border-t border-gray-600 mt-8 pt-8 text-center text-gray-400 text-sm">
          <p>© 2026 Group 1. This is an academic project for educational purposes.</p>
        </div>
      </div>
    </footer>
  );
}