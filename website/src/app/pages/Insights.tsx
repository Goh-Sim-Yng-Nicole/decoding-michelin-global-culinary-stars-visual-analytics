import { TrendingUp, Scale, Gem, MapPin, UtensilsCrossed, AlertTriangle, ClipboardList, ExternalLink, BarChart3, MessageSquare, Cloud } from 'lucide-react';

export function Insights() {
  return (
    <div className="min-h-screen bg-white">
      {/* Header */}
      <section className="border-b border-gray-200 bg-[#F9F8F6]">
        <div className="max-w-7xl mx-auto px-4 sm:px-8 py-10 sm:py-20 text-center">
          <div className="inline-block mb-4 sm:mb-6">
            <div className="flex items-center gap-2 text-xs sm:text-sm text-gray-500 uppercase tracking-widest">
              <div className="w-8 sm:w-12 h-px bg-gray-300"></div>
              <span>A Data-Driven Narrative</span>
              <div className="w-8 sm:w-12 h-px bg-gray-300"></div>
            </div>
          </div>
          <h1 className="text-3xl sm:text-4xl md:text-5xl font-bold mb-4 sm:mb-6 text-[#2B2B2B]">
            The Story Behind the Stars
          </h1>
          <p className="text-base sm:text-lg md:text-xl text-gray-600 leading-relaxed font-light max-w-4xl mx-auto">
            A comprehensive investigation exploring the truth about Michelin's prestige in Singapore
          </p>
        </div>
      </section>

      {/* Story Flow */}
      <div className="max-w-7xl mx-auto px-4 sm:px-8 py-12 sm:py-20">

        {/* Chapter 1: Dashboard 1: Overall (The Prestige Landscape) */}
        <div className="mb-20 sm:mb-32 border-b border-gray-200 pb-20 sm:pb-32">
          <div className="flex flex-col sm:flex-row items-start gap-4 sm:gap-6 mb-12">
            <div className="flex-shrink-0 w-12 h-12 sm:w-16 sm:h-16 bg-[#C8102E] text-white flex items-center justify-center font-bold text-xl sm:text-2xl">
              1
            </div>
            <div className="flex-1 w-full">
              <h2 className="text-2xl sm:text-3xl font-bold text-[#2B2B2B] mb-8">
                The Prestige Landscape
              </h2>
              
              <div className="bg-[#F9F8F6] border-l-4 border-[#C8102E] p-8 sm:p-10 mb-12">
                <p className="text-xl sm:text-2xl font-medium text-[#2B2B2B] leading-relaxed italic">
                  "Who gets the Michelin awards, what do they serve, and where are they located?"
                </p>
                <div className="mt-4 text-sm text-gray-500 uppercase tracking-widest">— Establishing the Baseline</div>
              </div>

              <div className="text-gray-700 text-base sm:text-lg leading-relaxed space-y-8">
                <p>
                  To understand Michelin's influence in Singapore, we first mapped the baseline distribution of awards. 
                  Our geo-spatial analysis revealed a stark concentration of prestige: most Michelin-listed restaurants 
                  cluster in central areas such as Orchard and Telok Ayer, with a noticeable void in the North and West. 
                  While starred establishments are almost entirely islanded in these central hubs, Bib Gourmand and 
                  Selected restaurants show a slightly more democratic spread.
                </p>
                
                <div className="grid sm:grid-cols-2 gap-8 my-12">
                  <div className="bg-white border-t-2 border-[#C8102E] shadow-lg p-8">
                    <div className="text-4xl font-bold text-[#2B2B2B] mb-2 flex items-center gap-3">
                      <MapPin className="w-8 h-8 text-[#C8102E]" />
                      Central <span className="text-xl font-medium text-gray-400">Hubs</span>
                    </div>
                    <div className="text-[#C8102E] text-xs font-bold uppercase tracking-widest mb-4">Location Density</div>
                    <p className="text-sm text-gray-600 leading-relaxed">
                      Michelin-listed restaurants cluster in central areas such as Orchard and Telok Ayer, highlighting 
                      a geographic barrier for many Singaporeans who live further out.
                    </p>
                  </div>
                  <div className="bg-white border-t-2 border-[#C8102E] shadow-lg p-8">
                    <div className="text-4xl font-bold text-[#2B2B2B] mb-2 flex items-center gap-3">
                      <UtensilsCrossed className="w-8 h-8 text-[#C8102E]" />
                      Street <span className="text-xl font-medium text-gray-400">Food</span>
                    </div>
                    <div className="text-[#C8102E] text-xs font-bold uppercase tracking-widest mb-4">Cultural Performance</div>
                    <p className="text-sm text-gray-600 leading-relaxed">
                      "Street Food" is one of the largest cuisine categories receiving awards, demonstrating that in 
                      Singapore, quality and craftsmanship are not limited by price or setting.
                    </p>
                  </div>
                </div>

                <p>
                  This distribution highlights that while high-end dining is gated in the city center, 
                  good quality food remains accessible. Many affordable restaurants are recognized under the 
                  Bib Gourmand and Selected categories. However, the data also suggests that the North and West 
                  may harbor "hidden local gems"—establishments that provide excellence yet remain outside the 
                  Michelin spotlight.
                </p>

                <div className="bg-[#2B2B2B] text-white p-8 rounded-sm">
                  <div className="flex items-center gap-4 mb-4">
                    <MessageSquare className="w-6 h-6 text-[#C8102E]" />
                    <h4 className="text-lg font-bold">Consumer Verdict</h4>
                  </div>
                  <p className="text-gray-300 text-base sm:text-lg leading-relaxed font-light">
                    Customer perception data confirms that starred restaurants consistently achieve higher satisfaction 
                    ratings (mostly above 4.0), while Bib Gourmand and Selected venues typically hover between 
                    3 to 4—still above average, but reflecting a different service tier.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Chapter 2: Customer Review Word Cloud (The Voice of the Diners) */}
        <div className="mb-20 sm:mb-32 border-b border-gray-200 pb-20 sm:pb-32">
          <div className="flex flex-col sm:flex-row items-start gap-4 sm:gap-6 mb-12">
            <div className="flex-shrink-0 w-12 h-12 sm:w-16 sm:h-16 bg-[#C8102E] text-white flex items-center justify-center font-bold text-xl sm:text-2xl">
              2
            </div>
            <div className="flex-1 w-full">
              <h2 className="text-2xl sm:text-3xl font-bold text-[#2B2B2B] mb-8">
                The Voice of the Diners
              </h2>
              
              <div className="bg-[#F9F8F6] border-l-4 border-[#C8102E] p-8 sm:p-10 mb-12">
                <p className="text-xl sm:text-2xl font-medium text-[#2B2B2B] leading-relaxed italic">
                  "What do diners actually say and care about?"
                </p>
                <div className="mt-4 text-sm text-gray-500 uppercase tracking-widest">— The Human Element</div>
              </div>

              <div className="text-gray-700 text-base sm:text-lg leading-relaxed space-y-8">
                <p>
                  This analysis serves as a transitional lens between the overview of Singapore's Michelin landscape 
                  and the detailed analysis that follows. Rather than presenting aggregated scores, it surfaces the 
                  unfiltered voice of diners, extracting the most frequently mentioned words from over 2,000 
                  restaurants across the island.
                </p>

                <div className="bg-white border-t-2 border-[#C8102E] shadow-lg p-8 my-12">
                  <div className="text-4xl font-bold text-[#2B2B2B] mb-2 flex items-center gap-3">
                    <Cloud className="w-8 h-8 text-[#C8102E]" />
                    Linguistic <span className="text-xl font-medium text-gray-400">Patterns</span>
                  </div>
                  <div className="text-[#C8102E] text-xs font-bold uppercase tracking-widest mb-6">Review Corpus Analysis</div>
                  
                  <p className="text-sm text-gray-600 leading-relaxed mb-6">
                    <span className="font-bold text-[#2B2B2B]">"Service"</span> emerges as the most dominant word 
                    across all reviews, establishing hospitality as the primary dimension through which diners 
                    evaluate their experience, reinforced by the frequent co-occurrence of "friendly" and "attentive".
                  </p>
                  
                  <div className="grid sm:grid-cols-2 gap-6">
                    <div className="p-5 bg-[#F9F8F6] border-l-2 border-[#C8102E]">
                      <h4 className="font-bold text-[#2B2B2B] text-sm mb-2 uppercase tracking-wider">Food-Forward Culture</h4>
                      <p className="text-xs text-gray-500 leading-relaxed">
                        High-frequency terms like "soup", "chicken", "rice", and "stall" reflect Singapore's 
                        hawker-centric dining culture, appearing even in reviews for Michelin-recognized venues.
                      </p>
                    </div>
                    <div className="p-5 bg-[#F9F8F6] border-l-2 border-[#C8102E]">
                      <h4 className="font-bold text-[#2B2B2B] text-sm mb-2 uppercase tracking-wider">The Michelin Effect</h4>
                      <p className="text-xs text-gray-500 leading-relaxed">
                        The word "Michelin" itself is prominent in reviews, suggesting it functions as an active 
                        reference point that shapes diner expectations before they even sit down.
                      </p>
                    </div>
                  </div>
                </div>

                <p>
                  Value-oriented terminology—such as <span className="font-bold text-[#2B2B2B]">"price", "worth", and "portion"</span>—indicates 
                  that cost-value assessment is a recurring dimension of diner evaluation, even within a corpus that 
                  skews predominantly positive with affirmative descriptors like "delicious" and "amazing". These linguistic 
                  patterns establish the sentiment baseline for the quantified scores examined in following dashboards.
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Chapter 3: Dashboard 2: Taste and Service (The Experience) */}
        <div className="mb-20 sm:mb-32 border-b border-gray-200 pb-20 sm:pb-32">
          <div className="flex flex-col sm:flex-row items-start gap-4 sm:gap-6 mb-12">
            <div className="flex-shrink-0 w-12 h-12 sm:w-16 sm:h-16 bg-[#C8102E] text-white flex items-center justify-center font-bold text-xl sm:text-2xl">
              3
            </div>
            <div className="flex-1 w-full">
              <h2 className="text-2xl sm:text-3xl font-bold text-[#2B2B2B] mb-8">
                The Michelin Experience
              </h2>
              
              <div className="bg-[#F9F8F6] border-l-4 border-[#C8102E] p-8 sm:p-10 mb-12">
                <p className="text-xl sm:text-2xl font-medium text-[#2B2B2B] leading-relaxed italic">
                  "Do Michelin-recognized restaurants deliver a superior dining experience from the perspective of customer sentiment?"
                </p>
                <div className="mt-4 text-sm text-gray-500 uppercase tracking-widest">— Taste vs. Service</div>
              </div>

              <div className="text-gray-700 text-base sm:text-lg leading-relaxed space-y-8">
                <p>
                  Reputation is built on two pillars: the plate and the person. Our second dashboard evaluates
                  whether Michelin-recognized restaurants deliver a prestige dining experience across taste and
                  service. By combining cuisine-level rankings, a bi-variate experience matrix, and a group-level
                  sentiment comparison, we provide a multidimensional assessment of whether formal culinary
                  recognition corresponds with perceived experiential quality.
                </p>

                <div className="border-y border-gray-100 py-10 my-10">
                  <h4 className="text-[#C8102E] font-bold uppercase tracking-widest text-xs mb-6 text-center">The Taste Leaders</h4>
                  <div className="flex flex-wrap justify-center gap-4">
                    {['Shopping Mall', 'Private Dining', 'Brazilian', 'Turkish', 'Scandinavian'].map((cuisine) => (
                      <span key={cuisine} className="px-6 py-3 bg-gray-50 border border-gray-200 text-base font-semibold rounded-full text-gray-700">
                        {cuisine}
                      </span>
                    ))}
                  </div>
                  <p className="text-sm text-center mt-6 text-gray-500 italic px-4">
                    Niche, specialized, and experiential dining categories dominate taste sentiment — taste
                    excellence is not exclusive to Michelin-recognized cuisines. Several non-Michelin categories
                    outperform traditional fine dining, suggesting diner evaluations are shaped significantly
                    by the nature and specialization of the cuisine itself.
                  </p>
                </div>

                <h3 className="text-xl sm:text-2xl font-bold text-[#2B2B2B]">The Experience Matrix</h3>
                <p>
                  The Experience Matrix plots each restaurant by taste sentiment on the horizontal axis and
                  service sentiment on the vertical axis, with dot size proportional to review volume. Benchmark
                  lines at approximately 0.87 for taste and 0.63 for service divide the chart into four
                  performance zones. Starred restaurants cluster densely in the upper-right high-performance
                  quadrant, confirming consistently above-average performance on both dimensions. Bib Gourmand
                  establishments, however, show a markedly different distribution — while many achieve strong
                  taste scores, they are substantially more dispersed along the service axis, with a significant
                  portion falling below the service average. This confirms that taste and service do not move
                  in tandem across Michelin tiers, and that consistent service delivery is the key differentiator
                  between the top and middle tiers of Michelin recognition.
                </p>

                <div className="bg-white border-t-2 border-[#C8102E] shadow-lg p-8 my-12">
                  <div className="text-4xl font-bold text-[#2B2B2B] mb-2 flex items-center gap-3">
                    <BarChart3 className="w-8 h-8 text-[#C8102E]" />
                    Taste <span className="text-xl font-medium text-gray-400">&gt;</span> Service
                  </div>
                  <div className="text-[#C8102E] text-xs font-bold uppercase tracking-widest mb-6">Sentiment Profiler</div>

                  <div className="space-y-6 text-sm text-gray-600 leading-relaxed">
                    <p>
                      The dumbbell chart quantifies the taste-service gap across three groups. Starred restaurants
                      record the strongest and most balanced performance, with the <span className="font-bold text-[#2B2B2B]">narrowest gap of just 0.11</span> between
                      taste and service — the tightest of all groups.
                    </p>
                    <div className="grid grid-cols-3 gap-4">
                      <div className="p-5 bg-[#F9F8F6]">
                        <div className="text-[#C8102E] font-bold text-xl">0.9036 / 0.7934</div>
                        <div className="text-xs text-gray-500 uppercase font-bold mt-1">Starred (Taste / Service)</div>
                        <div className="text-xs text-gray-400 mt-1">Gap: 0.11</div>
                      </div>
                      <div className="p-5 bg-[#F9F8F6]">
                        <div className="text-gray-700 font-bold text-xl">0.8752 / 0.6419</div>
                        <div className="text-xs text-gray-500 uppercase font-bold mt-1">Non-Michelin (Taste / Service)</div>
                        <div className="text-xs text-gray-400 mt-1">Gap: 0.23</div>
                      </div>
                      <div className="p-5 bg-[#F9F8F6]">
                        <div className="text-gray-400 font-bold text-xl">0.8477 / 0.5358</div>
                        <div className="text-xs text-gray-500 uppercase font-bold mt-1">Bib Gourmand (Taste / Service)</div>
                        <div className="text-xs text-gray-400 mt-1">Gap: 0.31</div>
                      </div>
                    </div>
                    <p className="text-gray-500 italic mt-4">
                      Bib Gourmand records the widest gap of 0.31 — its service score of 0.5358 falls 0.11 points
                      below even non-Michelin establishments, despite carrying formal Michelin recognition.
                    </p>
                  </div>
                </div>

                <p>
                  While starred restaurants justify their recognition through consistently strong performance across
                  both dimensions, the Bib Gourmand tier reveals a structural imbalance: culinary quality that meets
                  Michelin standards paired with hospitality that falls short of even the broader non-Michelin market.
                  This decoupling of food and service quality within a formally recognized tier underscores a core
                  finding — in Singapore's dining landscape, a Michelin recognition is not a reliable guarantee of a
                  well-rounded experience. It is consistent service delivery, and not culinary achievement alone, that
                  defines the restaurants diners return to.
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Chapter 4: Dashboard 3: Price and Value (The Financial Reality) */}
        <div className="mb-20 sm:mb-32 border-b border-gray-200 pb-20 sm:pb-32">
          <div className="flex flex-col sm:flex-row items-start gap-4 sm:gap-6 mb-12">
            <div className="flex-shrink-0 w-12 h-12 sm:w-16 sm:h-16 bg-[#C8102E] text-white flex items-center justify-center font-bold text-xl sm:text-2xl">
              4
            </div>
            <div className="flex-1 w-full">
              <h2 className="text-2xl sm:text-3xl font-bold text-[#2B2B2B] mb-8">
                The Financial Reality
              </h2>
              
              <div className="bg-[#F9F8F6] border-l-4 border-[#C8102E] p-8 sm:p-10 mb-12">
                <p className="text-xl sm:text-2xl font-medium text-[#2B2B2B] leading-relaxed italic">
                  "Is the price justified, and where do diners get the best 'bang for their buck'?"
                </p>
                <div className="mt-4 text-sm text-gray-500 uppercase tracking-widest">— Deconstructing Price vs. Value</div>
              </div>

              <div className="text-gray-700 text-base sm:text-lg leading-relaxed space-y-8">
                <p>
                  A common assumption in fine dining is that higher prices signify more value. Our third dashboard 
                  counters this narrative. By juxtaposing sentiment analysis of Google Reviews against official 
                  household expenditure data, we uncover a structural economic barrier that effectively excludes 
                  many Singaporeans from starred dining.
                </p>

                <h3 className="text-xl sm:text-2xl font-bold text-[#2B2B2B]">The Affordability Cliff</h3>
                <p>
                  The transition from Bib Gourmand to 1-Star dining is more than a culinary step up—it's a 
                  financial cliff. With a median cost of <span className="font-bold text-[#2B2B2B]">$120 per pax</span>, 
                  a single dinner at a 1-star restaurant exceeds the entire monthly restaurant budget of a 
                  bottom-quintile (Q1) household ($99.50). For most Singaporeans, starred dining is a 
                  significant financial event, not a regular occurrence.
                </p>

                <div className="grid sm:grid-cols-2 gap-8 my-12">
                  <div className="bg-white border-t-2 border-[#C8102E] shadow-lg p-8">
                    <div className="text-4xl font-bold text-[#2B2B2B] mb-2 flex items-center gap-3">
                      <Gem className="w-8 h-8 text-[#C8102E]" />
                      58.3%
                    </div>
                    <div className="text-[#C8102E] text-xs font-bold uppercase tracking-widest mb-4">Hidden Gems</div>
                    <p className="text-sm text-gray-600 leading-relaxed">
                      The majority of Singapore's dining landscape offers excellent value at reasonable prices 
                      ($ or $$), proving excellence is everywhere.
                    </p>
                  </div>
                  <div className="bg-white border-t-2 border-[#C8102E] shadow-lg p-8">
                    <div className="text-4xl font-bold text-[#2B2B2B] mb-2 flex items-center gap-3">
                      <TrendingUp className="w-8 h-8 text-[#C8102E]" />
                      4.9%
                    </div>
                    <div className="text-[#C8102E] text-xs font-bold uppercase tracking-widest mb-4">Tourist Traps</div>
                    <p className="text-sm text-gray-600 leading-relaxed">
                      A small segment, but one disproportionately concentrated with Michelin-starred establishments 
                      where prestige doesn't match sentiment.
                    </p>
                  </div>
                </div>

                <h3 className="text-xl sm:text-2xl font-bold text-[#2B2B2B]">The "Trap" of Prestige</h3>
                <p>
                  Our quadrant analysis reveals a counterintuitive finding: most restaurants holding a formal 
                  Michelin star are represented in the <span className="font-bold text-[#2B2B2B]">Tourist Trap</span> quadrant—high-priced 
                  establishments scoring below the 70% value threshold. This indicates that the premium commanded 
                  by starred restaurants is not consistently validated by diners' sentiment.
                </p>

                <div className="bg-[#2B2B2B] text-white p-10 rounded-sm my-12">
                  <h4 className="text-lg font-bold mb-6 border-b border-gray-700 pb-4">The Final Verdict on Value</h4>
                  <div className="space-y-6">
                    <p className="text-gray-300 text-base sm:text-lg leading-relaxed font-light">
                      The mid-range casual dining segment (<span className="text-white font-medium">$$ / ~$60 per pax</span>) 
                      emerges as Singapore's optimal value proposition. These establishments record the highest 
                      average value sentiment scores (75.5%), substantially exceeding both the hawker tier and the 
                      ultra-premium fine dining tiers.
                    </p>
                    <div className="bg-white/5 p-6 border-l-2 border-[#C8102E]">
                      <p className="text-sm italic text-gray-400">
                        "The Michelin premium is real, but the value return is not consistently justified."
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Chapter 5: Dashboard 4: Hygiene (The Safety Blind Spot) */}
        <div className="mb-20 sm:mb-32 border-b border-gray-200 pb-20 sm:pb-32">
          <div className="flex flex-col sm:flex-row items-start gap-4 sm:gap-6 mb-12">
            <div className="flex-shrink-0 w-12 h-12 sm:w-16 sm:h-16 bg-[#C8102E] text-white flex items-center justify-center font-bold text-xl sm:text-2xl">
              5
            </div>
            <div className="flex-1 w-full">
              <h2 className="text-2xl sm:text-3xl font-bold text-[#2B2B2B] mb-8">
                The Safety Blind Spot
              </h2>
              
              <div className="bg-[#F9F8F6] border-l-4 border-[#C8102E] p-8 sm:p-10 mb-12">
                <p className="text-xl sm:text-2xl font-medium text-[#2B2B2B] leading-relaxed italic">
                  "Does paying hundreds of dollars guarantee a spotless kitchen? We stripped away the glamour to audit basic food safety."
                </p>
                <div className="mt-4 text-sm text-gray-500 uppercase tracking-widest">— Auditing SFA Hygiene Grades</div>
              </div>

              <div className="text-gray-700 text-base sm:text-lg leading-relaxed space-y-8">
                <p>
                  Michelin recognition is based on the quality of ingredients and technique, but it famously silent on 
                  kitchen hygiene. Our fourth dashboard bridges this gap by mapping official Singapore Food Agency (SFA) 
                  hygiene grades against Michelin prestige. The results expose potential health risks that a star symbol 
                  often obscures.
                </p>

                <div className="bg-white border-t-2 border-[#C8102E] shadow-lg p-8 my-12">
                  <div className="text-4xl font-bold text-[#2B2B2B] mb-2 flex items-center gap-3">
                    <ClipboardList className="w-8 h-8 text-[#C8102E]" />
                    Audit <span className="text-xl font-medium text-gray-400">Target: Grade A</span>
                  </div>
                  <div className="text-[#C8102E] text-xs font-bold uppercase tracking-widest mb-6">Hygiene Audit</div>
                  
                  <div className="space-y-6 text-sm text-gray-600 leading-relaxed">
                    <p>
                      While the majority of Michelin-listed restaurants achieve top standards, lower hygiene 
                      grades are not as rare as one might expect. 
                    </p>
                    <ul className="space-y-4 text-sm marker:text-[#C8102E]">
                      <li><span className="font-bold text-[#2B2B2B]">Grade A Dominance:</span> All 3-star restaurants maintain Grade A standards, representing the pinnacle of both safety and prestige.</li>
                      <li><span className="font-bold text-[#2B2B2B]">The Starred Exception:</span> A noticeable number of 1-star and 2-star restaurants hold B-grade ratings, suggesting a gap between the dining room and the kitchen.</li>
                      <li><span className="font-bold text-[#2B2B2B]">Street Food Reliability:</span> Surprisingly, the Street Food category maintains a high proportion of Grade A status, proving safety is not gated by price.</li>
                    </ul>
                  </div>
                </div>

                <h3 className="text-xl sm:text-2xl font-bold text-[#2B2B2B]">Price vs. Hygiene</h3>
                <p>
                  Our analysis shows that hygiene standards are remarkably consistent across different price levels. 
                  Affordable ($) restaurants still offer many A-grade options, making safe and quality food accessible 
                  to all. However, the presence of B-grades in the more expensive tiers indicates that <span className="font-bold text-[#2B2B2B]">higher costs do not guarantee better food safety.</span>
                </p>

                <div className="bg-[#2B2B2B] text-white p-8 rounded-sm my-12">
                  <div className="flex items-start gap-4">
                    <AlertTriangle className="w-6 h-6 text-[#C8102E] flex-shrink-0 mt-1" />
                    <div>
                      <h4 className="text-lg font-bold mb-2">The "Fragile Star" Risk</h4>
                      <p className="text-gray-300 text-sm sm:text-base leading-relaxed font-light">
                        We identified establishments where high ratings and prestigious awards coexist with 
                        lower hygiene grades. These "Fragile Stars" prove the necessity of integrating 
                        regulatory data into dining decisions—reputation alone is not a sufficient predictor of safety.
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Chapter 6: Dashboard 5: Smart Diner Recommender (The Actionable Finale) */}
        <div className="mb-20 sm:mb-32">
          <div className="flex flex-col sm:flex-row items-start gap-4 sm:gap-6 mb-12">
            <div className="flex-shrink-0 w-12 h-12 sm:w-16 sm:h-16 bg-[#C8102E] text-white flex items-center justify-center font-bold text-xl sm:text-2xl">
              6
            </div>
            <div className="flex-1 w-full">
              <h2 className="text-2xl sm:text-3xl font-bold text-[#2B2B2B] mb-8">
                The Actionable Finale
              </h2>
              
              <div className="bg-[#F9F8F6] border-l-4 border-[#C8102E] p-8 sm:p-10 mb-12">
                <p className="text-xl sm:text-2xl font-medium text-[#2B2B2B] leading-relaxed italic">
                  "Empowering diners to find safe, high-value alternatives based on their own priorities."
                </p>
                <div className="mt-4 text-sm text-gray-500 uppercase tracking-widest">— The Smart Diner Recommender</div>
              </div>

              <div className="text-gray-700 text-base sm:text-lg leading-relaxed space-y-8">
                <p>
                  Synthesizing our multi-dimensional analysis, our final dashboard serves as an interactive 
                  discovery tool. We believe that a "black box" algorithm shouldn't define quality for you. 
                  Instead, we provide the data and the tools for you to define it yourself.
                </p>

                <div className="grid gap-8 my-12">
                  <div className="flex gap-6 items-start text-base sm:text-lg">
                    <div className="flex-shrink-0 w-10 h-10 bg-[#F9F8F6] flex items-center justify-center rounded-full text-[#C8102E]">
                      <MapPin className="w-5 h-5" />
                    </div>
                    <div>
                      <h3 className="text-xl font-bold text-[#2B2B2B] mb-2">Interactive Discovery Map</h3>
                      <p className="text-sm sm:text-base text-gray-600 leading-relaxed">
                        Select a Michelin venue and instantly view a walking-distance radius populated with 
                        highly-rated, non-Michelin alternatives. Escape the "Tourist Traps" and find the 
                        true local favorites just a few streets away.
                      </p>
                    </div>
                  </div>

                  <div className="flex gap-6 items-start text-base sm:text-lg">
                    <div className="flex-shrink-0 w-10 h-10 bg-[#F9F8F6] flex items-center justify-center rounded-full text-[#C8102E]">
                      <Scale className="w-5 h-5" />
                    </div>
                    <div>
                      <h3 className="text-xl font-bold text-[#2B2B2B] mb-2">Direct Comparison Tool</h3>
                      <p className="text-sm sm:text-base text-gray-600 leading-relaxed">
                        How does that famous star actually stack up? Our dynamic bar charts provide a 
                        side-by-side evaluation of Taste, Value, Service, and Hygiene against any 
                        counterpart of your choice.
                      </p>
                    </div>
                  </div>

                  <div className="flex gap-6 items-start text-base sm:text-lg">
                    <div className="flex-shrink-0 w-10 h-10 bg-[#F9F8F6] flex items-center justify-center rounded-full text-[#C8102E]">
                      <ClipboardList className="w-5 h-5" />
                    </div>
                    <div>
                      <h3 className="text-xl font-bold text-[#2B2B2B] mb-2">Personalized Recommender</h3>
                      <p className="text-sm sm:text-base text-gray-600 leading-relaxed">
                        Adjust our parameter sliders to re-sort suggestions based on your own weighting. 
                        Whether you prioritize price, safety, or pure culinary sentiment, our platform 
                        democratizes discovery.
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Conclusion */}
        <div className="bg-[#2B2B2B] text-white p-10 sm:p-20 relative overflow-hidden">
          <div className="absolute top-0 right-0 w-64 h-64 bg-[#C8102E]/10 -mr-32 -mt-32 rounded-full blur-3xl"></div>
          <div className="max-w-5xl mx-auto text-center relative z-10">
            <h2 className="text-4xl sm:text-5xl font-bold mb-10">The Verdict</h2>
            <div className="space-y-8 text-lg sm:text-xl text-gray-300 font-light leading-relaxed">
              <p>
                Our visual analytics approach effectively <span className="text-white font-medium">demystifies the aura of the Michelin Guide</span> in Singapore. 
                We discovered that a Michelin award does not unconditionally guarantee superior service, 
                optimal value, or even baseline kitchen hygiene.
              </p>
              <p>
                The presence of "Fragile Stars"—prestigious but unhygienic or poorly-rated establishments—proves 
                the necessity of a data-driven approach to dining. Conversely, our tool successfully surfaces 
                "True Gems," democratizing the discovery of high-quality food.
              </p>
            </div>
            
            <div className="mt-16 pt-16 border-t border-gray-800">
              <p className="text-3xl sm:text-4xl font-bold mb-6 text-white italic">
                "Stars may guide you, but data empowers you."
              </p>
              <p className="text-gray-400 max-w-2xl mx-auto leading-relaxed">
                Make informed decisions. Explore our dashboards to find restaurants that match
                YOUR priorities, not just Michelin's.
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Data Sources Section */}
      <section className="bg-[#F9F8F6] border-t border-gray-200 py-16 sm:py-24">
        <div className="max-w-7xl mx-auto px-4 sm:px-8">
          <div className="text-center mb-12 sm:mb-16">
            <h2 className="text-3xl sm:text-4xl font-bold text-[#2B2B2B] mb-4">
              Data Sources
            </h2>
            <div className="w-16 h-1 bg-[#C8102E] mx-auto"></div>
          </div>

          <div className="grid sm:grid-cols-2 gap-6 sm:gap-8">
            <a
              href="https://www.kaggle.com/datasets/ngshiheng/michelin-guide-restaurants-2021"
              target="_blank"
              rel="noopener noreferrer"
              className="bg-white border border-gray-200 p-6 sm:p-8 hover:border-[#C8102E] transition-colors group"
            >
              <div className="flex items-start justify-between mb-4">
                <h3 className="font-semibold text-lg sm:text-xl text-[#2B2B2B] group-hover:text-[#C8102E] transition-colors">
                  Kaggle - Michelin Guide Restaurants
                </h3>
                <ExternalLink className="w-5 h-5 text-gray-400 group-hover:text-[#C8102E] transition-colors flex-shrink-0" strokeWidth={1.5} />
              </div>
              <p className="text-gray-600 text-sm sm:text-base leading-relaxed mb-3">
                Main dataset containing restaurant details, cuisine types, and award information
              </p>
              <p className="text-[10px] sm:text-sm text-gray-500 font-mono break-all">
                kaggle.com/datasets/ngshiheng/michelin-guide-restaurants-2021
              </p>
            </a>

            <a
              href="https://apify.com/tri_angle/restaurant-review-aggregator/api/javascript"
              target="_blank"
              rel="noopener noreferrer"
              className="bg-white border border-gray-200 p-6 sm:p-8 hover:border-[#C8102E] transition-colors group"
            >
              <div className="flex items-start justify-between mb-4">
                <h3 className="font-semibold text-lg sm:text-xl text-[#2B2B2B] group-hover:text-[#C8102E] transition-colors">
                  Apify - Restaurant Review Aggregator
                </h3>
                <ExternalLink className="w-5 h-5 text-gray-400 group-hover:text-[#C8102E] transition-colors flex-shrink-0" strokeWidth={1.5} />
              </div>
              <p className="text-gray-600 text-sm sm:text-base leading-relaxed mb-3">
                API for collecting customer reviews from Google Maps and TripAdvisor
              </p>
              <p className="text-[10px] sm:text-sm text-gray-500 font-mono break-all">
                apify.com/tri_angle/restaurant-review-aggregator
              </p>
            </a>

            <a
              href="https://data.gov.sg/datasets/d_546a95c5e6a0a264a82247ec107a0629/view"
              target="_blank"
              rel="noopener noreferrer"
              className="bg-white border border-gray-200 p-6 sm:p-8 hover:border-[#C8102E] transition-colors group"
            >
              <div className="flex items-start justify-between mb-4">
                <h3 className="font-semibold text-lg sm:text-xl text-[#2B2B2B] group-hover:text-[#C8102E] transition-colors">
                  Data.gov.sg - Certificate Grading Info
                </h3>
                <ExternalLink className="w-5 h-5 text-gray-400 group-hover:text-[#C8102E] transition-colors flex-shrink-0" strokeWidth={1.5} />
              </div>
              <p className="text-gray-600 text-sm sm:text-base leading-relaxed mb-3">
                Licensed eating establishments hygiene grading data under SAFE framework (GeoJSON)
              </p>
              <p className="text-[10px] sm:text-sm text-gray-500 font-mono break-all">
                data.gov.sg/datasets/d_546a95c5e6a0a264a82247ec107a0629
              </p>
            </a>

            <a
              href="https://www.singstat.gov.sg/find-data/search-by-theme/households/household-expenditure/visualising-data/household-expenditure-survey-dashboard"
              target="_blank"
              rel="noopener noreferrer"
              className="bg-white border border-gray-200 p-6 sm:p-8 hover:border-[#C8102E] transition-colors group"
            >
              <div className="flex items-start justify-between mb-4">
                <h3 className="font-semibold text-lg sm:text-xl text-[#2B2B2B] group-hover:text-[#C8102E] transition-colors">
                  Singstat - Household Expenditure Survey
                </h3>
                <ExternalLink className="w-5 h-5 text-gray-400 group-hover:text-[#C8102E] transition-colors flex-shrink-0" strokeWidth={1.5} />
              </div>
              <p className="text-gray-600 text-sm sm:text-base leading-relaxed mb-3">
                Dashboard for household expenditure data providing affordability context
              </p>
              <p className="text-[10px] sm:text-sm text-gray-500 font-mono break-all">
                singstat.gov.sg/find-data/household-expenditure
              </p>
            </a>
          </div>
        </div>
      </section>
    </div>
  );
}