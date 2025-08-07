async function loadChartData() {
    const chartContainer = document.getElementById('candlestickChart');
    
    console.log('Starting to load portfolio performance data...');
    try {
        // Fetch portfolio performance data from the server
        const response = await fetch('/api/portfolio/performance');
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const portfolioData = await response.json();
        console.log('Received portfolio data:', portfolioData);
        
        if (portfolioData.error) {
            console.error('Error in portfolio data:', portfolioData.error);
            throw new Error(portfolioData.error);
        }
        
        // Process the data for the chart
        const labels = portfolioData.dates || [];
        const values = portfolioData.values || [];
        
        console.log('Processed labels:', labels);
        console.log('Processed values:', values);
        
        if (labels.length === 0 || values.length === 0) {
            console.error('No data available in the response');
            throw new Error('No data available');
        }
        
        // Create chart data
        const chartData = {
            labels: labels,
            datasets: [{
                label: 'Portfolio Value',
                data: values,
                borderColor: '#06b6d4',
                backgroundColor: 'rgba(99,102,241,0.10)',
                borderWidth: 3,
                fill: true,
                tension: 0.4,
                pointBackgroundColor: '#6366f1',
                pointBorderColor: '#fff',
                pointBorderWidth: 2,
                pointRadius: 3,
                pointHoverRadius: 5
            }]
        };

        // Create the chart
        const candlestickCtx = chartContainer.getContext('2d');
        new Chart(candlestickCtx, {
            type: 'line',
            data: chartData,
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        mode: 'index',
                        intersect: false,
                        backgroundColor: 'rgba(255, 255, 255, 0.95)',
                        titleColor: '#1f2937',
                        bodyColor: '#1f2937',
                        borderColor: '#6366f1',
                        borderWidth: 2,
                        cornerRadius: 12,
                        titleFont: {
                            weight: 'bold'
                        },
                        bodyFont: {
                            weight: '500'
                        },
                        callbacks: {
                            label: function(context) {
                                let label = context.dataset.label || '';
                                if (label) {
                                    label += ': ';
                                }
                                if (context.parsed.y !== null) {
                                    label += new Intl.NumberFormat('en-US', { 
                                        style: 'currency', 
                                        currency: 'USD',
                                        minimumFractionDigits: 2,
                                        maximumFractionDigits: 2
                                    }).format(context.parsed.y);
                                }
                                return label;
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        display: true,
                        title: {
                            display: true,
                            text: 'Date',
                            color: '#374151', // text-gray-700
                            font: {
                                weight: '600',
                                size: 14
                            }
                        },
                        grid: {
                            display: false
                        },
                        ticks: {
                            color: '#6b7280',
                            font: {
                                weight: '500'
                            }
                        }
                    },
                    y: {
                        display: true,
                        title: {
                            display: true,
                            text: 'Portfolio Value (USD)',
                            color: '#374151',
                            font: {
                                weight: '600',
                                size: 14
                            }
                        },
                        grid: {
                            color: 'rgba(99,102,241,0.1)',
                            lineWidth: 1
                        },
                        ticks: {
                            color: '#6b7280',
                            font: {
                                weight: '500'
                            },
                            callback: function(value) {
                                return new Intl.NumberFormat('en-US', { 
                                    style: 'currency', 
                                    currency: 'USD',
                                    minimumFractionDigits: 0,
                                    maximumFractionDigits: 0
                                }).format(value);
                            }
                        }
                    }
                }
                
            }
        });
    } catch (error) {
        console.error('Error loading portfolio performance data:', error);
        // Fallback to a simple message if data loading fails
        chartContainer.parentElement.innerHTML = `
            <div class="text-center p-8">
                <p class="text-red-500">Unable to load performance data. ${error.message || 'Please try again later.'}</p>
            </div>
        `;
    }
};

document.addEventListener('DOMContentLoaded', () => loadChartData());