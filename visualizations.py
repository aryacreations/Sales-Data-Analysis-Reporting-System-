"""
Sales Data Visualization Module
Creates charts and graphs for sales analysis
"""

import matplotlib.pyplot as plt
import numpy as np
from sales_analysis import SalesAnalyzer

class SalesVisualizer:
    """Class for creating sales visualizations"""
    
    def __init__(self, analyzer=None):
        """Initialize visualizer with analyzer instance"""
        self.analyzer = analyzer if analyzer else SalesAnalyzer()
        if self.analyzer.df is None:
            self.analyzer.load_data()
    
    def plot_monthly_revenue_trend(self, save_path='monthly_revenue_trend.png'):
        """Plot monthly revenue trends"""
        monthly = self.analyzer.calculate_monthly_trends()
        
        plt.figure(figsize=(14, 6))
        
        # Convert period to string for plotting
        months = [str(m) for m in monthly.index]
        revenue = monthly['revenue'].values
        
        plt.plot(months, revenue, marker='o', linewidth=2, markersize=8, color='#2E86AB')
        plt.fill_between(range(len(months)), revenue, alpha=0.3, color='#2E86AB')
        
        # Add average line
        avg_revenue = np.mean(revenue)
        plt.axhline(y=avg_revenue, color='#A23B72', linestyle='--', linewidth=2, label=f'Average: ${avg_revenue:,.0f}')
        
        plt.title('Monthly Revenue Trend', fontsize=16, fontweight='bold', pad=20)
        plt.xlabel('Month', fontsize=12, fontweight='bold')
        plt.ylabel('Revenue ($)', fontsize=12, fontweight='bold')
        plt.xticks(rotation=45, ha='right')
        plt.grid(True, alpha=0.3, linestyle='--')
        plt.legend(fontsize=10)
        plt.tight_layout()
        
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Saved monthly revenue trend chart to {save_path}")
        plt.close()
    
    def plot_top_products(self, top_n=10, save_path='top_products.png'):
        """Plot top products by revenue"""
        products = self.analyzer.find_best_selling_products(top_n)
        
        plt.figure(figsize=(12, 8))
        
        # Create horizontal bar chart
        y_pos = np.arange(len(products))
        revenue = products['revenue'].values
        product_names = products.index.tolist()
        
        # Create color gradient
        colors = plt.cm.viridis(np.linspace(0.3, 0.9, len(products)))
        
        bars = plt.barh(y_pos, revenue, color=colors)
        
        # Add value labels
        for i, (bar, val) in enumerate(zip(bars, revenue)):
            plt.text(val, i, f' ${val:,.0f}', va='center', fontweight='bold', fontsize=9)
        
        plt.yticks(y_pos, product_names)
        plt.xlabel('Revenue ($)', fontsize=12, fontweight='bold')
        plt.title(f'Top {top_n} Products by Revenue', fontsize=16, fontweight='bold', pad=20)
        plt.grid(True, alpha=0.3, axis='x', linestyle='--')
        plt.tight_layout()
        
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Saved top products chart to {save_path}")
        plt.close()
    
    def plot_sales_distribution(self, save_path='sales_distribution.png'):
        """Plot sales value distribution"""
        if self.analyzer.df is None:
            self.analyzer.load_data()
        
        revenue = self.analyzer.df['quantity'] * self.analyzer.df['price']
        
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        
        # Histogram
        axes[0].hist(revenue, bins=50, color='#F18F01', alpha=0.7, edgecolor='black')
        axes[0].axvline(np.mean(revenue), color='#C73E1D', linestyle='--', linewidth=2, label=f'Mean: ${np.mean(revenue):.2f}')
        axes[0].axvline(np.median(revenue), color='#6A994E', linestyle='--', linewidth=2, label=f'Median: ${np.median(revenue):.2f}')
        axes[0].set_xlabel('Sale Value ($)', fontsize=11, fontweight='bold')
        axes[0].set_ylabel('Frequency', fontsize=11, fontweight='bold')
        axes[0].set_title('Sales Value Distribution', fontsize=13, fontweight='bold')
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)
        
        # Box plot
        box = axes[1].boxplot(revenue, vert=True, patch_artist=True)
        box['boxes'][0].set_facecolor('#A7C957')
        box['boxes'][0].set_alpha(0.7)
        axes[1].set_ylabel('Sale Value ($)', fontsize=11, fontweight='bold')
        axes[1].set_title('Sales Value Box Plot', fontsize=13, fontweight='bold')
        axes[1].grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Saved sales distribution chart to {save_path}")
        plt.close()
    
    def plot_quantity_vs_revenue(self, save_path='quantity_vs_revenue.png'):
        """Plot quantity sold vs revenue by product"""
        products = self.analyzer.find_best_selling_products(15)
        
        fig, ax1 = plt.subplots(figsize=(14, 7))
        
        x = np.arange(len(products))
        product_names = products.index.tolist()
        
        # Bar chart for quantity
        ax1.bar(x - 0.2, products['quantity'], width=0.4, label='Quantity Sold', color='#4ECDC4', alpha=0.8)
        ax1.set_xlabel('Product', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Quantity Sold', fontsize=12, fontweight='bold', color='#4ECDC4')
        ax1.tick_params(axis='y', labelcolor='#4ECDC4')
        ax1.set_xticks(x)
        ax1.set_xticklabels(product_names, rotation=45, ha='right')
        
        # Line chart for revenue
        ax2 = ax1.twinx()
        ax2.plot(x, products['revenue'], marker='o', linewidth=2, markersize=8, label='Revenue', color='#FF6B6B')
        ax2.set_ylabel('Revenue ($)', fontsize=12, fontweight='bold', color='#FF6B6B')
        ax2.tick_params(axis='y', labelcolor='#FF6B6B')
        
        plt.title('Quantity Sold vs Revenue by Product', fontsize=16, fontweight='bold', pad=20)
        
        # Add legends
        lines1, labels1 = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper right')
        
        ax1.grid(True, alpha=0.3, axis='y')
        plt.tight_layout()
        
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Saved quantity vs revenue chart to {save_path}")
        plt.close()
    
    def generate_all_visualizations(self):
        """Generate all visualizations"""
        print("\n📊 Generating Visualizations...\n")
        
        self.plot_monthly_revenue_trend()
        self.plot_top_products()
        self.plot_sales_distribution()
        self.plot_quantity_vs_revenue()
        
        print("\n✅ All visualizations generated successfully!")

def main():
    """Main function to generate visualizations"""
    visualizer = SalesVisualizer()
    visualizer.generate_all_visualizations()

if __name__ == '__main__':
    main()
