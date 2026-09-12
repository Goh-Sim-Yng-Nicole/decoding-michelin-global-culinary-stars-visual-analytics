import { Link } from 'react-router';
import { DollarSign, Star, ShieldCheck } from 'lucide-react';
const michelinImage = "https://images.unsplash.com/photo-1514362545857-3bc16c4c7d1b?auto=format&fit=crop&q=80&w=2070";

export function Home() {
  return (
    <div className="min-h-screen bg-white">
      {/* Hero Section - Editorial Style */}
      <section className="border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-8 py-12 sm:py-20">
          <div className="text-center max-w-4xl mx-auto mb-10 sm:mb-16">
            <div className="inline-block mb-6">
              <div className="flex items-center gap-2 text-sm text-gray-500 uppercase tracking-widest mb-3">
                <div className="w-8 sm:w-12 h-px bg-gray-300"></div>
                <span>A Data-Driven Investigation</span>
                <div className="w-8 sm:w-12 h-px bg-gray-300"></div>
              </div>
            </div>
            <h1 className="text-4xl sm:text-5xl md:text-6xl font-bold mb-4 sm:mb-8 text-[#2B2B2B] leading-tight">
              En-tire-ly Overrated?
            </h1>
            <p className="text-lg sm:text-xl md:text-2xl text-gray-600 mb-8 sm:mb-12 leading-relaxed font-light">
              Uncovering whether Michelin recognition in Singapore accurately reflects
              dining quality through customer experience, food safety, and value.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link
                to="/dashboards"
                className="bg-[#C8102E] text-white px-8 sm:px-10 py-3 sm:py-4 text-xs sm:text-sm font-medium tracking-wide uppercase hover:bg-[#A00D25] transition-colors text-center"
              >
                View Dashboards
              </Link>
              <Link
                to="/insights"
                className="border-2 border-[#2B2B2B] text-[#2B2B2B] px-8 sm:px-10 py-3 sm:py-4 text-xs sm:text-sm font-medium tracking-wide uppercase hover:bg-[#2B2B2B] hover:text-white transition-colors text-center"
              >
                Explore Insights
              </Link>
            </div>
          </div>

          <div className="max-w-4xl mx-auto">
            <img
              src={michelinImage}
              alt="Michelin Guide"
              className="w-full rounded-sm shadow-lg"
            />
          </div>
        </div>
      </section>

      {/* What is Michelin Guide */}
      <section className="py-16 sm:py-24 border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-8">
          <div className="text-center mb-12 sm:mb-16">
            <h2 className="text-3xl sm:text-4xl font-bold text-[#2B2B2B] mb-4">
              What is the Michelin Guide?
            </h2>
            <div className="w-16 h-1 bg-[#C8102E] mx-auto"></div>
          </div>

          <div className="grid md:grid-cols-2 gap-10 sm:gap-16 mb-16">
            <div className="space-y-6">
              <p className="text-base sm:text-lg leading-relaxed text-gray-700">
                The Michelin Guide was established in the early 20th century and formalized
                its star rating system in 1931. Today, it is one of the most globally prestigious
                restaurant rating systems.
              </p>
              <p className="text-base sm:text-lg leading-relaxed text-gray-700">
                Restaurants are awarded one to three stars from "worth a stop," "worth a detour,"
                and "worth a journey." As of now, Michelin recognizes over 3,700 restaurants worldwide,
                including 42 in Singapore.
              </p>
            </div>

            <div className="bg-[#F9F8F6] p-6 sm:p-10 border border-gray-200">
              <h3 className="text-sm font-semibold mb-6 sm:mb-8 text-[#2B2B2B] uppercase tracking-wide">Star Ratings</h3>
              <div className="space-y-6 sm:space-y-8">
                <div className="flex items-start gap-4">
                  <img src="/michelin_icons/michelin-star.png" alt="1 Michelin Star" className="w-6 h-6 sm:w-8 sm:h-8 flex-shrink-0 mt-1" />
                  <div>
                    <h4 className="font-semibold text-sm sm:text-base mb-1 sm:mb-2 text-[#2B2B2B]">One Star</h4>
                    <p className="text-gray-600 text-xs sm:text-sm leading-relaxed">High quality cooking, worth a stop</p>
                  </div>
                </div>
                <div className="flex items-start gap-4">
                  <div className="flex gap-0.5 sm:gap-1 flex-shrink-0 mt-1">
                    <img src="/michelin_icons/michelin-star.png" alt="Michelin Star" className="w-6 h-6 sm:w-8 sm:h-8" />
                    <img src="/michelin_icons/michelin-star.png" alt="Michelin Star" className="w-6 h-6 sm:w-8 sm:h-8" />
                  </div>
                  <div>
                    <h4 className="font-semibold text-sm sm:text-base mb-1 sm:mb-2 text-[#2B2B2B]">Two Stars</h4>
                    <p className="text-gray-600 text-xs sm:text-sm leading-relaxed">Excellent cooking, worth a detour</p>
                  </div>
                </div>
                <div className="flex items-start gap-4">
                  <div className="flex gap-0.5 sm:gap-1 flex-shrink-0 mt-1">
                    <img src="/michelin_icons/michelin-star.png" alt="Michelin Star" className="w-6 h-6 sm:w-8 sm:h-8" />
                    <img src="/michelin_icons/michelin-star.png" alt="Michelin Star" className="w-6 h-6 sm:w-8 sm:h-8" />
                    <img src="/michelin_icons/michelin-star.png" alt="Michelin Star" className="w-6 h-6 sm:w-8 sm:h-8" />
                  </div>
                  <div>
                    <h4 className="font-semibold text-sm sm:text-base mb-1 sm:mb-2 text-[#2B2B2B]">Three Stars</h4>
                    <p className="text-gray-600 text-xs sm:text-sm leading-relaxed">Exceptional cuisine, worth a special journey</p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div className="bg-[#F4C100]/10 border-l-4 border-[#F4C100] p-6 sm:p-10">
            <h3 className="text-lg sm:text-xl font-semibold mb-4 text-[#2B2B2B]">Bib Gourmand</h3>
            <p className="text-base sm:text-lg text-gray-700 leading-relaxed">
              The Guide also includes the Bib Gourmand, which highlights restaurants offering
              good quality food at relatively affordable prices. Because of this reputation,
              many diners trust Michelin awards as a signal of quality — but that trust is
              exactly what we want to examine.
            </p>
          </div>
        </div>
      </section>

      {/* Why This Matters */}
      <section className="py-16 sm:py-24 bg-[#F9F8F6] border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-8">
          <div className="text-center mb-12 sm:mb-16">
            <h2 className="text-3xl sm:text-4xl font-bold text-[#2B2B2B] mb-4">
              Why Should You Care?
            </h2>
            <div className="w-16 h-1 bg-[#C8102E] mx-auto"></div>
          </div>

          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6 sm:gap-8">
            <div className="bg-white p-8 sm:p-10 border border-gray-200">
              <div className="mb-6">
                <DollarSign className="w-10 h-10 sm:w-12 sm:h-12 text-[#C8102E]" strokeWidth={1.5} />
              </div>
              <h3 className="text-lg sm:text-xl font-semibold mb-4 text-[#2B2B2B]">Cost Matters</h3>
              <p className="text-gray-600 text-sm sm:text-base leading-relaxed">
                Singapore is ranked as the second most expensive country in the world for
                Michelin-starred dining, with tasting menus often costing several hundred
                dollars per person. Such high prices create very high expectations.
              </p>
            </div>

            <div className="bg-white p-8 sm:p-10 border border-gray-200">
              <div className="mb-6">
                <Star className="w-10 h-10 sm:w-12 sm:h-12 text-[#C8102E]" strokeWidth={1.5} />
              </div>
              <h3 className="text-lg sm:text-xl font-semibold mb-4 text-[#2B2B2B]">Experience Gaps</h3>
              <p className="text-gray-600 text-sm sm:text-base leading-relaxed">
                Michelin recognition does not always reflect everyday customer experience.
                Online reviews show that even Michelin-recognized restaurants receive
                complaints about service consistency, value, and quality.
              </p>
            </div>

            <div className="bg-white p-8 sm:p-10 border border-gray-200">
              <div className="mb-6">
                <ShieldCheck className="w-10 h-10 sm:w-12 sm:h-12 text-[#C8102E]" strokeWidth={1.5} />
              </div>
              <h3 className="text-lg sm:text-xl font-semibold mb-4 text-[#2B2B2B]">Safety Transparency</h3>
              <p className="text-gray-600 text-sm sm:text-base leading-relaxed">
                There is limited transparency around food safety. Singapore's strict SAFE
                framework hygiene grades are not considered in Michelin awards, which may
                cause diners to prioritize prestige over safety.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Our Approach */}
      <section className="py-16 sm:py-24 border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-8">
          <div className="text-center mb-12 sm:mb-16">
            <h2 className="text-3xl sm:text-4xl font-bold text-[#2B2B2B] mb-4">
              Our Data-Driven Approach
            </h2>
            <div className="w-16 h-1 bg-[#C8102E] mx-auto"></div>
          </div>

          <div className="grid md:grid-cols-2 gap-8 sm:gap-12">
            <div className="border border-gray-200 p-6 sm:p-10">
              <h3 className="text-xs sm:text-sm font-semibold mb-6 sm:mb-8 text-[#C8102E] uppercase tracking-wide">Data Sources</h3>
              <ul className="space-y-4 sm:space-y-5">
                <li className="flex items-start gap-4">
                  <div className="w-1.5 h-1.5 bg-[#C8102E] rounded-full mt-2 sm:mt-2.5 flex-shrink-0"></div>
                  <div>
                    <div className="font-semibold text-sm sm:text-base text-[#2B2B2B] mb-0.5 sm:mb-1">Michelin World Guide</div>
                    <div className="text-gray-600 text-xs sm:text-sm">From Kaggle for restaurant details, cuisine types, and awards</div>
                  </div>
                </li>
                <li className="flex items-start gap-4">
                  <div className="w-1.5 h-1.5 bg-[#C8102E] rounded-full mt-2 sm:mt-2.5 flex-shrink-0"></div>
                  <div>
                    <div className="font-semibold text-sm sm:text-base text-[#2B2B2B] mb-0.5 sm:mb-1">Online Reviews</div>
                    <div className="text-gray-600 text-xs sm:text-sm">From Google Maps and TripAdvisor using Apify</div>
                  </div>
                </li>
                <li className="flex items-start gap-4">
                  <div className="w-1.5 h-1.5 bg-[#C8102E] rounded-full mt-2 sm:mt-2.5 flex-shrink-0"></div>
                  <div>
                    <div className="font-semibold text-sm sm:text-base text-[#2B2B2B] mb-0.5 sm:mb-1">SFA Hygiene Grading</div>
                    <div className="text-gray-600 text-xs sm:text-sm">Data under the SAFE framework</div>
                  </div>
                </li>
                <li className="flex items-start gap-4">
                  <div className="w-1.5 h-1.5 bg-[#C8102E] rounded-full mt-2 sm:mt-2.5 flex-shrink-0"></div>
                  <div>
                    <div className="font-semibold text-sm sm:text-base text-[#2B2B2B] mb-0.5 sm:mb-1">SingStat Data</div>
                    <div className="text-gray-600 text-xs sm:text-sm">On household expenditure for affordability context</div>
                  </div>
                </li>
              </ul>
            </div>

            <div className="border border-gray-200 p-6 sm:p-10">
              <h3 className="text-xs sm:text-sm font-semibold mb-6 sm:mb-8 text-[#C8102E] uppercase tracking-wide">Analysis Methods</h3>
              <ul className="space-y-4 sm:space-y-5">
                <li className="flex items-start gap-4">
                  <div className="w-1.5 h-1.5 bg-[#C8102E] rounded-full mt-2 sm:mt-2.5 flex-shrink-0"></div>
                  <div>
                    <div className="font-semibold text-sm sm:text-base text-[#2B2B2B] mb-0.5 sm:mb-1">Sentiment Analysis</div>
                    <div className="text-gray-600 text-xs sm:text-sm">To quantify customer perceptions of food quality, service, and value</div>
                  </div>
                </li>
                <li className="flex items-start gap-4">
                  <div className="w-1.5 h-1.5 bg-[#C8102E] rounded-full mt-2 sm:mt-2.5 flex-shrink-0"></div>
                  <div>
                    <div className="font-semibold text-sm sm:text-base text-[#2B2B2B] mb-0.5 sm:mb-1">Hygiene Mapping</div>
                    <div className="text-gray-600 text-xs sm:text-sm">Using Python to identify potential safety gaps</div>
                  </div>
                </li>
                <li className="flex items-start gap-4">
                  <div className="w-1.5 h-1.5 bg-[#C8102E] rounded-full mt-2 sm:mt-2.5 flex-shrink-0"></div>
                  <div>
                    <div className="font-semibold text-sm sm:text-base text-[#2B2B2B] mb-0.5 sm:mb-1">Affordability Analysis</div>
                    <div className="text-gray-600 text-xs sm:text-sm">To evaluate true value beyond Michelin price categories</div>
                  </div>
                </li>
                <li className="flex items-start gap-4">
                  <div className="w-1.5 h-1.5 bg-[#C8102E] rounded-full mt-2 sm:mt-2.5 flex-shrink-0"></div>
                  <div>
                    <div className="font-semibold text-sm sm:text-base text-[#2B2B2B] mb-0.5 sm:mb-1">Tableau Visualizations</div>
                    <div className="text-gray-600 text-xs sm:text-sm">For interactive comparisons of prestige, sentiment, safety, and value</div>
                  </div>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* Project Goals */}
      <section className="py-16 sm:py-24 bg-[#2B2B2B] text-white">
        <div className="max-w-4xl mx-auto px-4 sm:px-8 text-center">
          <h2 className="text-3xl sm:text-4xl font-bold mb-6 sm:mb-8">Our Mission</h2>
          <p className="text-lg sm:text-xl leading-relaxed mb-10 sm:mb-12 text-gray-300 font-light">
            We transform prestige, sentiment, safety, and affordability into transparent
            visual analysis. By doing so, we aim to help diners move beyond reputation and
            make better-informed dining decisions.
          </p>
          <Link
            to="/insights"
            className="inline-block bg-[#C8102E] text-white px-10 sm:px-12 py-3 sm:py-4 text-xs sm:text-sm font-medium tracking-wide uppercase hover:bg-[#A00D25] transition-colors"
          >
            Discover Our Insights
          </Link>
        </div>
      </section>
    </div>
  );
}