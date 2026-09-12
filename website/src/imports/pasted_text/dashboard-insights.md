
Dashboard 1: The Culinary Landscape (Overview)
It provides a high-level overview of the Singapore Michelin scene.
Distribution of Awards: Most entries are "Selected Restaurants" or "Bib Gourmand," with a smaller elite group of Starred restaurants.
Top 10 Cuisines: This highlights Singapore's strength in Street Food and Chinese cuisine, which dominate the Michelin guide.
Taste vs. Value Sentiment: It shows that while Starred restaurants (often more expensive) have high taste scores, many Bib Gourmands offer higher "Value Sentiment," proving you don't always have to pay more for a satisfying experience.
Price Tier Distribution: Most Michelin-recognized spots are actually in the lower price tiers ($ and $$), debunking the myth that Michelin is only for the ultra-wealthy.




Dashboard 2: Sentiment & Quality Charts
Bubble Chart: Taste vs Service vs Value
X-axis: Taste Sentiment
Y-axis: Service Sentiment
Bubble Size: Average spending (from Price category)
Color: Award level
Story: "Where does each restaurant excel? Which offers the best overall experience?"
Insight: Identify overpriced restaurants (high spending, low sentiment) vs hidden gems (low spending, high sentiment)
Horizontal Bar Chart: Top Cuisines by Taste Sentiment
Story: "Which cuisines deliver the best-tasting dishes?"
Metric: Average Taste Sentiment by cuisine
Ranking: Highest to lowest
Insight: Reveals quality perception beyond awards
Scatter: Price vs Value Sentiment
X-axis: Price Range (actual values)
Y-axis: Value Sentiment
Story: "Which restaurants offer the best bang for your buck?"
Insight: Find affordable excellence and identify overpriced spots



Dashboard 3: Geographic Visualizations
Map with Markers
Color coding: By Michelin award or price range
Size: By sentiment score or price
Story: "Where should you go in Singapore to find Michelin restaurants?"
Insight: Concentration in CBD (Marina Bay), Tanjong Pagar, Orchard
Use case: Dining guides, neighborhood recommendations
Heatmap (Grid)
Metric: Count of restaurants per location/district
Story: "Which neighborhoods punch above their weight in dining?"
Finding: CBD-heavy, but emerging scenes in Clementi, East Coast

Dashboard 4: Comparison Charts
Grouped Bar: Award Type + Price Range
Story: "Do Michelin stars cost more?"
Insight: Compare average price across award tiers
Finding: 3-star ≠ always 4 prices; value exists at all levels
Horizontal Stacked Bar: Cuisine + Award Distribution
Story: "Which cuisines most represented in top awards?"
X-axis: Count of restaurants
Segments: Award levels (3-star, 2-star, etc.)
Insight: French, Chinese, Japanese dominance in fine dining
Comparison Table: Award Type Performance
Columns: Award Type, Count, Avg Price, Avg Taste, Avg Service, Avg Value, Avg Hygiene
Story: "How do different Michelin tiers perform across quality metrics?"

Chart 5: Time-Independent Relationship Charts
Correlation Matrix / Heatmap
Variables: Price, Taste Sentiment, Service Sentiment, Value Sentiment, Affordability Ratio
Story: "What relationships exist between price, quality, and value?"
Insight: Surprising finding: Low price doesn't always mean low taste sentiment




Jillian
 FOUNDATIONAL VISUALRating Distribution (Box Plot)
Shows how ratings differ between Michelin and non-Michelin restaurants, highlighting spread, outliers, and overlap rather than just averages. Helps test whether Michelin status consistently correlates with higher quality.
Price vs Rating Scatter Plot
Plots price level against rating to examine whether more expensive restaurants actually deliver better quality. Challenges the assumption that higher cost equals better experience.
Sentiment vs Rating Scatter Plot
Compares numerical ratings with sentiment scores derived from reviews. Reveals whether structured ratings align with unstructured customer feedback.
Review Volume Distribution (Histogram)
Shows distribution of number of reviews across restaurants. Helps identify popularity bias and whether highly reviewed restaurants dominate perception.
Geospatial Map of Restaurants
Displays restaurant locations using latitude and longitude. Adds spatial context and allows users to explore geographic patterns in quality and safety.

COMPARATIVE ANALYTICS (CORE PROJECT FOCUS)
Michelin vs Non-Michelin Comparison (Bar Chart)
Compares average rating, sentiment, and safety between Michelin and non-Michelin restaurants. Forms the core argument of whether Michelin status reflects true quality.
Value Score Comparison (Box Plot)
Uses value score (rating ÷ price level) to compare efficiency of spending. Highlights whether Michelin restaurants justify their higher prices.
Safety vs Price Scatter Plot
Examines relationship between hygiene grade and price level. Tests whether more expensive restaurants are actually safer.
Sentiment vs Safety Scatter Plot
Compares customer sentiment with hygiene grade. Reveals whether perceived quality aligns with actual food safety standards.
Michelin Award Breakdown (Bar Chart)
Breaks Michelin restaurants into Star, Bib Gourmand, and Plate categories. Adds nuance beyond simple Michelin vs non-Michelin comparison.

ADVANCED VISUAL ANALYTICS
Hidden Gem Quadrant Chart ⭐
Quadrant chart of rating vs price to identify high-quality, low-cost non-Michelin restaurants. Provides actionable insights for discovering underrated dining options.
Hidden Gem Ranking Table
Ranks restaurants using a composite Hidden Gem score. Transforms analysis into a recommendation system rather than just observation.
Parallel Coordinates Plot
Displays multiple variables (rating, sentiment, safety, price) across axes. Enables multivariate comparison of restaurant performance.
Correlation Heatmap
Shows relationships between variables like rating, sentiment, price, and safety. Helps uncover hidden patterns and dependencies.
Reputation Bubble Chart
Plots sentiment vs rating with size based on review volume. Combines multiple dimensions into one efficient visual.
Cuisine Performance Treemap
Breaks down restaurant performance by cuisine type. Shows which cuisines deliver better ratings, value, or safety.
Geographic Heatmap
Displays density of high-performing restaurants. Identifies clusters of quality dining locations.
Sentiment Distribution Histogram
Shows distribution of sentiment scores across all reviews. Reveals overall emotional landscape of dining experiences.

WOW-LEVEL VISUALS (FOR A+)
Michelin Value Paradox Chart ⭐
Box plot comparing value scores of Michelin vs non-Michelin restaurants. Highlights that prestige does not always equal better value.
Restaurant Reputation Radar ⭐
Radar chart comparing rating, sentiment, safety, and popularity. Provides a holistic profile of each restaurant’s strengths and weaknesses.
Opportunity Map ⭐
Map showing areas with high ratings but low Michelin presence. Identifies underserved regions and potential business opportunities.
Tourist Trap Detector ⭐
Identifies restaurants with high price but low rating/sentiment. Highlights overpriced or underperforming establishments.
Interactive Recommender Dashboard ⭐
Allows users to adjust weights (rating, price, safety, sentiment) to generate personalized restaurant recommendations. Turns dashboard into a decision-support tool.
Ranking Stability Analysis
Compares rankings based on rating vs sentiment. Evaluates consistency and reliability of different evaluation metrics.
Outlier Detection Plot
Highlights extreme performers (very high or very low). Helps identify anomalies that may be hidden in averages.

🧠 Suggested Story Flow (For Presentation)
Are Michelin restaurants actually better?
Is the price justified?
Are there better non-Michelin alternatives?
Does safety align with quality and perception?
Where should users actually go?








Kelsey

Rows: Award (Michelin status)
Columns: sfa_hygiene_grade (A, B, C)
Cell Value: Count of restaurants.
Why it works: It visually calls out if any Michelin-starred restaurants have "B" or "C" hygiene grades. This exposes the "safety gap" your project aims to bridge.

The Problem: even awarded restaurants receive complaints about value for money and service consistency.

The Visualization: Standard guides use generic ratings (e.g., 4.2 stars). use specific columns like value_excellent_pct to create a truly meaningful comparison. This leaderboard displays the Top 10 restaurants in terms of Value Excellence, meaning those with the absolute highest proportion of "Value: Excellent" reviews. This gives diners a data-driven, actionable ranking of what is "worthy" of their money and detour, not just what is prestigious, allowing them to filter by their actual priorities like cuisine and minimum safety standard.



This visualization will help you instantly grasp the distribution of Michelin recognition across different cuisine types and how much "buzz" (reviews) each category generates.
How to Construct This in Tableau:
Structure (Rows/Columns/Detail): Arrange Award, Cuisine, and Name hierarchically.
Size: Drag review_count to the 'Size' mark. This determines how large the rectangle is. Larger rectangles have more reviews.
Color: Drag avg_stars to the 'Color' mark.
Color Palette (Crucial): Use a diverging palette (e.g., Red-to-Green, or your dashboard colors) to show poor performance (red) versus excellent performance (green).
Label: Add Cuisine and Name to the 'Label' mark.
You will immediately see if most Michelin reviews in Singapore are concentrated in one specific cuisine (e.g., "Nonya") or award level (e.g., "Bib Gourmand").





It uses the Latitude and Longitude data from your Michelin dataset to plot every recognized restaurant in Singapore on a map. When a user navigates the dashboard  and hovers their cursor over a specific point, a dynamic "tooltip" appears.
The tooltip is a miniature visualization of the sentiment analysis. 



This graph shows the relationship between restaurant sentiment (customer experience) and price level using a scatter plot.
Each circle represents a restaurant:
X-axis (Price Score): how expensive the restaurant is
Y-axis (Sentiment): overall customer rating or experience
Color: performance (green = better sentiment, red = worse)
Size: number of reviews
When a user clicks on a restaurant, a tooltip appears with key details (rating, value score, hygiene grade) and direct links to Google Maps and the restaurant’s website, allowing users to immediately take action.




Nicole
Dashboard 1: The Prestige Landscape (to set the scene)
Award Tier Distribution (Donut Chart)
Cuisine Breakdown by Award Tier (Stacked Bar)
Geospatial Map (Tableau Symbol Map)


Dashboard 2: Stars v.s. Sentiment
Sentiment Radar by Award Tier (Radar / Spider Chart)
Average Sentiment Scores by Tier (Grouped Bar Chart)
Google Stars Rating vs Value Score (Scatter Plot)
Google Review Word Cloud




Dashboard 3: The Safety Blind Spot
Hygiene Grade by Award Tier (100% Stacked Bar)
Fragile Stars Bubble Chart (Price vs Hygiene)
Safety Penalty Heatmap (Award Tier × Price)



Dashboard 4: Affordability & Value
True Affordability Ratio by Award Tier (Dot Plot / Gradient Strip)
Value Score Distribution by Price Tier (Box Plot)



Dashboard 5: Verdict - True Gems
Tourist Trap vs True Gem Quadrant (Scatter)
Top 15 True Gems Ranking (Lollipop Chart)

Dashboard 6: Michelin vs Non-Michelin
All Dimensions vs Non-Michelin (Grouped Bar Chart)
Hygiene Grade by Award Group (100% Stacked Bar)




Swen
Ideas
Visual concept is an old newspaper aesthetic.



Dashboard
Chart
Dashboard 1
Michelin Landscape, Geospatial Distribution

Establish baseline of where Michelin Restaurants are, what they serve
Culinary Map (Point Map)
Map of Singapore plotting all Michelin restaurants in the dataset
Colour/icon code by Award Status (i.e. 3 star, 2 star, 1 star, Bib Gourmand) → can also include unawarded restaurants
Allow tourists to filter by neighbourhood, cuisine
When a listing (restaurant) is clicked, the user is able to view the website/google result of the restaurant → URL can be taken from dataset
Award Distribution by Cuisine
Bar chart with Cuisine Type by Restaurant count
Show if Michelin shows a bias/preference towards certain cuisines in Singapore
Filter Panel
Cuisine
Location/Region → neighbourhood, east-west side, etc. hierarchy
Price tier → affordability
Hygiene level
Michelin Star Ratings: How Do They Work? | The Official Wasserstrom Blog

Dashboard 2
Prestige vs Reality

Does Michelin = good food and good hygiene?
Expectation vs Reality Scatter Plot
Price/Tier vs Overall Sentiment Score
Same colours/icon code to represent Michelin Status as culinary map
Show that if you want higher quality Michelin score, often unaffordable
Safety Audit
Bar chart, Michelin Award tier vs % of total 
Color code by the SFA Hygiene Grade
Michelin restaurants maintain higher regulatory hygiene standards than non-awarded restaurants?
Sentiment Breakdown
Box and whisker plot, award tier against sentiment scores
Separate plots for taste, service, value
Variance within award tier for each category/requirement
Dashboard 3
Economic Context & Affordability

How affordable are these restaurants?
True Affordability Index
Average cost of meal at specific restaurant tier, reference line for average monthly expenditure for Singaporean households (?)
Compare restaurant costs against daily spending habits, highlight inaccessibility of high quality restaurants
Value for Money
Overall Sentiment Score vs Estimated cost per pax
Reference line at median to create quadrants
Tourist traps = high cost, low value (top left)
Value gems = low cost, high value (bottom right)
Dashboard 4
Recommender

Allow user to choose their own restaurants, can show the user recommended restaurant based on their own criteria or based on alternatives to a selected Michelin restaurant

Parameter sliders criteria
Hygiene
Price
Taste

Michelin Matcher Dropdown that allows users to select a specific Michelin-awarded restaurant they are considering visiting
Discovery Map
Map focused on neighbourhood of chosen Michelin restaurant
Within search radius, display recommended non-Michelin alternatives
How to make: 
Use Tableau's MAKEPOINT and DISTANCE or BUFFER spatial functions. 
The selected Michelin restaurant acts as the center point (maybe shaped with the Michelin logo). 
Shaded circle shows the search radius. Inside that radius, Chef hats/Fork and Spoon represent the recommended non-Michelin alternatives.
Alternative Leaderboard
Table ranking restaurants shown on the map
Comparison Bar Chart
When a user clicks a listing on the map, the chart updates to show direct comparison between selected Michelin restaurant and chosen alternative
Show:
Taste
Value
Service
Hygiene



Styling Considerations
Michelin Guide Red: #C8102E (Use this for your top banner, main titles, and the Bib Gourmand category).
Michelin Star Gold: #F4C100 (Use this only for Starred restaurants. Do not use it for anything else, to preserve its meaning).
Guidebook Black/Charcoal: #2B2B2B (For primary text and chart axes).
"Crisp Page" Background: #F9F8F6 (Instead of harsh pure white, use an off-white/cream that mimics the high-quality paper of the physical guidebook).
The Stars: Use Michelin Star PNG
Bib Gourmand: Use the icon of the Michelin Man
The "Tire" (Playing on your title): For restaurants that are unawarded or severely downgraded in your "True Gem" leaderboard, use a subtle PNG of a tire.
The Map: On your Neighborhood Map, the selected Michelin restaurant should be the massive 6-pointed Gold Star, and the alternatives can be smaller, sleek map pins.
Like these ideas:

Your dashboard should look like the official Michelin Guide, but "vandalized" by an auditor.
The Guidebook Fonts: Use Serif font for all Restaurant Names and Dashboard Titles. This mimics the classic serif print of the physical book.
The Auditor's Markups (Optional but very cool): For your "Expectation vs. Reality" scatter plot, use Tableau's Annotation feature. Write the annotations in a font like Comic Sans or a handwriting font (if available), colored in Bright Red, pointing out the "Tourist Traps". It will look like an auditor scribbled on the Michelin Guide with a red pen.
Design your tooltips to look like high-end restaurant receipts.
RESTAURANT: <Restaurant Name>
MICHELIN TIER: <Star Rating>
---------------------------------
EXPECTED COST: ...... $<Price>
REALITY VALUE: ...... <Sentiment Score>/10
SFA HYGIENE: ........ Grade <Hygiene>
---------------------------------
VERDICT: <Calculated Overrated/Underrated field>


Since your title is "En-tire-ly Overrated," a subtle nod to Michelin's actual business (tires) is a great easter egg.
Instead of using plain solid lines to separate your charts or dashboard sections, you can create a thin image of tire tracks (in very light grey, almost transparent) and place it in an Image Object between your containers. It ties the visual analytics back to the project's clever name.
