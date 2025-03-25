import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
#Kavish Nag

# Load the dataset
file_path = "online_advertising_performance_data.csv"
try:
    df = pd.read_csv(file_path)
except Exception as e:
    print(f"Failed to load data: {e}")
    exit()

# Convert 'month' and 'day' into a proper datetime column
df['date'] = pd.to_datetime(df['month'].astype(str) + '-' + df['day'].astype(str) + '-2025')

# Display basic info
print(df.info())
print(df.head())

# Handling missing values
for col in df.columns:
    if df[col].dtype == 'object':
        df[col] = df[col].fillna('Unknown')
    elif df[col].dtype == 'int64' or df[col].dtype == 'float64':
        df[col] = df[col].fillna(0)

# 1. Trend in user engagement
plt.figure(figsize=(12, 5))
df.groupby('date')['user_engagement'].count().plot(title='User Engagement Trend')
plt.xlabel('Date')
plt.ylabel('User Engagement Count')
plt.show()

# 2. Impact of banner size on clicks
plt.figure(figsize=(10, 5))
sns.boxplot(x='banner', y='clicks', data=df)
plt.title('Effect of Banner Size on Clicks')
plt.xticks(rotation=45)
plt.show()

# 3. Placements with highest displays and clicks
displays_clicks = df.groupby('placement')[['displays', 'clicks']].sum().sort_values('displays', ascending=False)
print(displays_clicks.head())

# 4. Correlation between cost and revenue
plt.figure(figsize=(8, 5))
sns.scatterplot(x='cost', y='revenue', data=df)
plt.title('Cost vs Revenue')
plt.show()
print(df[['cost', 'revenue']].corr())

# 5. Average revenue per click
df['revenue_per_click'] = df['revenue'] / df['clicks'].replace(0, np.nan)
print(f"Average Revenue per Click: {df['revenue_per_click'].mean():.2f}")

# 6. Campaigns with highest post-click conversion rates
df['post_click_conversion_rate'] = df['post_click_conversions'] / df['clicks'].replace(0, np.nan)
campaign_conversion_rates = df.groupby('campaign_number')['post_click_conversion_rate'].mean().sort_values(
    ascending=False)
print(campaign_conversion_rates.head())

# 7. Trends in post-click sales amounts over time
plt.figure(figsize=(12, 5))
df.groupby('date')['post_click_sales_amount'].sum().plot(title='Post Click Sales Amount Over Time')
plt.xlabel('Date')
plt.ylabel('Sales Amount')
plt.show()

# 8. User engagement variation across banner sizes
sns.boxplot(x='banner', y='user_engagement', data=df)
plt.xticks(rotation=45)
plt.title('User Engagement by Banner Size')
plt.show()

# 9. Placements with highest post-click conversion rates
placement_conversion_rates = df.groupby('placement')['post_click_conversion_rate'].mean().sort_values(ascending=False)
print(placement_conversion_rates.head())

# 10. Seasonal patterns in displays and clicks
df['month_year'] = pd.to_datetime(df['month'].astype(str) + '-2025')
df.groupby('month_year')[['displays', 'clicks']].sum().plot(figsize=(12, 5), title='Monthly Displays and Clicks')
plt.xlabel('Month')
plt.ylabel('Count')
plt.legend(['Displays', 'Clicks'])
plt.show()

# 11. Correlation between user engagement and revenue
mapping = {'Low': 1, 'Medium': 2, 'High': 3}  
df['user_engagement_num'] = df['user_engagement'].map(mapping)
plt.figure(figsize=(8, 5))
sns.scatterplot(x='user_engagement_num', y='revenue', data=df)
plt.title('User Engagement vs Revenue')
plt.xlabel('User Engagement (Numerical)')
plt.show()
print(df[['user_engagement_num', 'revenue']].corr())

# 12. Outliers in cost, clicks, and revenue
plt.figure(figsize=(12, 5))
df[['cost', 'clicks', 'revenue']].boxplot()
plt.title('Outliers in Cost, Clicks, and Revenue')
plt.show()

# 13. Campaign effectiveness based on ad size and placement
effectiveness = df.groupby(['banner', 'placement'])[['revenue', 'cost']].sum()
effectiveness['ROI'] = effectiveness['revenue'] / effectiveness['cost'].replace(0, np.nan)
print(effectiveness.sort_values('ROI', ascending=False).head())

# 14. Best performing campaigns by ROI
campaign_roi = df.groupby('campaign_number')[['revenue', 'cost']].sum()
campaign_roi['ROI'] = campaign_roi['revenue'] / campaign_roi['cost'].replace(0, np.nan)
print(campaign_roi.sort_values('ROI', ascending=False).head())

# 15. Distribution of post-click conversions across placements
plt.figure(figsize=(10, 5))
sns.boxplot(x='placement', y='post_click_conversions', data=df)
plt.xticks(rotation=45)
plt.title('Post Click Conversions by Placement')
plt.show()

# 16. User engagement differences between weekdays and weekends
df['weekday'] = df['date'].dt.day_name()
weekday_engagement = df.groupby('weekday')['user_engagement'].count()
weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
weekday_engagement.loc[weekday_order].plot(kind='bar', figsize=(10, 5), title='User Engagement on Weekdays vs '
'Weekends')
plt.ylabel('User Engagement Count')
plt.show()

# 17. Cost per click (CPC) variation across campaigns and banners
df['CPC'] = df['cost'] / df['clicks'].replace(0, np.nan)
sns.boxplot(x='campaign_number', y='CPC', data=df)
plt.xticks(rotation=45)
plt.title('Cost per Click (CPC) by Campaign')
plt.show()
sns.boxplot(x='banner', y='CPC', data=df)
plt.xticks(rotation=45)
plt.title('Cost per Click (CPC) by Banner Size')
plt.show()
# 18. Cost-effective campaigns and placements for post-click conversions
campaign_conversion_cost = df.groupby('campaign_number')[['post_click_conversions', 'cost']].sum()
campaign_conversion_cost['cost_per_conversion'] = campaign_conversion_cost['cost'] / campaign_conversion_cost['post_'
'click_conversions'].replace(0, np.nan)
print(campaign_conversion_cost.sort_values('cost_per_conversion', ascending=True).head())
# 19. Trends in post-click conversion rates by day of the week
conversion_by_day = df.groupby('weekday')['post_click_conversion_rate'].mean()
weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
conversion_by_day.loc[weekday_order].plot(kind='bar', figsize=(10, 5), title='Post Click Conversion Rate by Day of'
' the Week')
plt.ylabel('Conversion Rate')
plt.show()
# 20. Campaign effectiveness across user engagement types
engagement_conversion = df.groupby('user_engagement')['post_click_conversions'].sum()
engagement_conversion.plot(kind='bar', figsize=(10, 5), title='Post Click Conversions by User Engagement Type')
plt.ylabel('Total Conversions')
plt.show()
