const ctx = document.getElementById('myChart').getContext('2d');

const myChart = new Chart(ctx, {
    type: 'bar',
    data: groceriesDataByCount.data,
    options: {
        indexAxis: 'y',
        scales: {
            x: {
                beginAtZero: true,
            },
        },
        elements: {
            bar: {
                borderWidth: 1,
            }
        },
        responsive: false,
        plugins: {
            legend: {
                position: 'right',
            },
            title: {
                display: true,
                text: 'Sorted by Count'
            },
            tooltip: {
                callbacks: {
                    footer: (tooltipItems) => {
                        return `cycle: ${Math.floor(groceriesDataByCount.cycle[tooltipItems[0].dataIndex])} days, `
                                +`date_list: ${groceriesDataByCount.date_list[tooltipItems[0].dataIndex].slice(0,5)}`;
                    }
                }
            }
        }
    },
});

const countSortBtn = document.getElementById("countSortBtn");
countSortBtn.onclick = () => {
    myChart.data = groceriesDataByCount.data;
    myChart.config.options.plugins.title.text = 'Sorted by Count';
    myChart.config.options.plugins.tooltip.callbacks.footer = (tooltipItems) => {
        return `cycle: ${Math.floor(groceriesDataByCount.cycle[tooltipItems[0].dataIndex])} days, `
                +`date_list: ${groceriesDataByCount.date_list[tooltipItems[0].dataIndex].slice(0,5)}`;
    }
    myChart.update();
}
const predictonSortBtn = document.getElementById("predictonSortBtn");
predictonSortBtn.onclick = () => {
    myChart.data = groceriesDataByPrediction.data;
    myChart.config.options.plugins.title.text = 'Sorted by Prediction based on Cycles';
    myChart.config.options.plugins.tooltip.callbacks.footer = (tooltipItems) => {
        return `cycle: ${Math.floor(groceriesDataByPrediction.cycle[tooltipItems[0].dataIndex])} days, `
                +`date_list: ${groceriesDataByPrediction.date_list[tooltipItems[0].dataIndex].slice(0,5)}`;
    }
    myChart.update();
}