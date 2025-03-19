color_palette = {
  'incomes' : ['#d8f3dc', '#b7e4c7', '#95d5b2', '#74c69d', '#52b788', '#40916c', '#2d6a4f', '#1b4332', '#081c15'], 
  'outcomes' : ['#ffba08', '#faa307', '#f48c06', '#e85d04', '#e85d04', '#dc2f02', '#d00000', '#9d0208', '#6a040f', '#370617', '#03071e']
}

function concat_uniques(array1, array2){
  return array1.concat(array2).filter((v,i,a)=>a.indexOf(v)==i)
}

document.addEventListener('DOMContentLoaded', () => {
      // Initilisation data
    async function init() {
      const data = await getFilteredData(['*'], ['*']);
      const incomeTimeSeriesData = {
          labels: data.incomes.months,
          datasets: [{
              label: 'Total Expenses Over Time',
              data: data.incomes.month_sums,
              borderColor: 'rgb(75, 192, 192)',
              tension: 0.1,
              backgroundColor: color_palette.incomes
          }]
      };
      const incomePieChartData = {
          labels: data.incomes.categories,
          datasets: [{
              label: 'Expenses by Category',
              data: data.incomes.categorie_sums,
              backgroundColor: color_palette.incomes,
              hoverOffset: 4
          }]
      };
      const outcomeTimeSeriesData = {
        labels: data.outcomes.months,
        datasets: [{
            label: 'Total Expenses Over Time',
            data: data.outcomes.month_sums,
            borderColor: 'rgb(75, 192, 192)',
            tension: 0.1,
            backgroundColor: color_palette.outcomes
        }]
      };
      const outcomePieChartData = {
          labels: data.outcomes.categories,
          datasets: [{
              label: 'Expenses by Category',
              data: data.outcomes.categorie_sums,
              backgroundColor: color_palette.outcomes,
              hoverOffset: 4
          }]
      };
    
      // Get chart contexts
      const incomeTimeSeriesCtx = document.getElementById('incomeTimeSeriesChart').getContext('2d');
      const incomePieChartCtx = document.getElementById('incomePieChart').getContext('2d');
      const outcomeTimeSeriesCtx = document.getElementById('outcomeTimeSeriesChart').getContext('2d');
      const outcomePieChartCtx = document.getElementById('outcomePieChart').getContext('2d');

      console.log(data.incomes.months)
      // Create charts
      const incomeTimeSeriesChart = new Chart(incomeTimeSeriesCtx, {
          type: 'bar',
          data: incomeTimeSeriesData,
          options: {
              responsive: true,
              maintainAspectRatio: false,
              scales: {
                  y: {
                      beginAtZero: true
                  }
              }
          }
      });
      const incomePieChart = new Chart(incomePieChartCtx, {
          type: 'pie',
          data: incomePieChartData,
          options: {
              responsive: true,
              maintainAspectRatio: false
          }
      });
      const outcomeTimeSeriesChart = new Chart(outcomeTimeSeriesCtx, {
        type: 'bar',
        data: outcomeTimeSeriesData,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
      });
      const outcomePieChart = new Chart(outcomePieChartCtx, {
          type: 'pie',
          data: outcomePieChartData,
          options: {
              responsive: true,
              maintainAspectRatio: false
          }
      });
      const availableCategories = concat_uniques(data.incomes.categories, data.outcomes.categories);
      const availableMonths = concat_uniques(data.incomes.months, data.outcomes.months);
  
      const categoryFiltersContainer = document.getElementById('category-filters');
      const monthFiltersContainer = document.getElementById('month-filters');
      function createFilterButtons(filters, container, filterType) {
          filters.forEach(filterName => {
              const button = document.createElement('button');
              button.classList.toggle('active'); // Initially active
              button.textContent = filterName;
              button.dataset.filterValue = filterName; // Store filter value
              button.dataset.filterType = filterType; // Store filter type
              button.addEventListener('click', handleFilterButtonClick);
              container.appendChild(button);
          });
      }
  
      createFilterButtons(availableCategories, categoryFiltersContainer, 'category');
      createFilterButtons(availableMonths, monthFiltersContainer, 'month');
      function handleFilterButtonClick(event) {
          const button = event.target;
          button.classList.toggle('active'); // Toggle active class for visual feedback
  
          const selectedCategories = Array.from(categoryFiltersContainer.querySelectorAll('button.active'))
              .map(btn => btn.dataset.filterValue);
          const selectedMonths = Array.from(monthFiltersContainer.querySelectorAll('button.active'))
              .map(btn => btn.dataset.filterValue);
  
          console.log('Selected Categories:', selectedCategories);
          console.log('Selected Months:', selectedMonths);
  
          updateChartsWithFilteredData(selectedCategories, selectedMonths); // Simulate update
      }
  
  
      // --- Chart Update with Filtered Data ---
      async function updateChartsWithFilteredData(selectedCategories, selectedMonths) {
          console.log('Chart update with filters:', selectedCategories, selectedMonths);
          const data = await getFilteredData(selectedCategories, selectedMonths)
          const incomeCategories = data.incomes.categories;
          const incomeCategorieSums = data.incomes.categorie_sums;
          const incomeMonths = data.incomes.months;
          const incomeMonthSums = data.incomes.month_sums;
          const outcomeCategories = data.outcomes.categories;
          const outcomeCategorieSums = data.outcomes.categorie_sums;
          const outcomeMonths = data.outcomes.months;
          const outcomeMonthSums = data.outcomes.month_sums;
          
          incomeTimeSeriesChart.data.datasets[0].data = incomeMonthSums;
          incomeTimeSeriesChart.data.labels = incomeMonths;
          incomeTimeSeriesChart.update()
          incomePieChart.data.datasets[0].data = incomeCategorieSums;
          incomePieChart.data.labels = incomeCategories;
          incomePieChart.update()
          outcomeTimeSeriesChart.data.datasets[0].data = outcomeMonthSums;
          outcomeTimeSeriesChart.data.labels = outcomeMonths;
          outcomeTimeSeriesChart.update()
          outcomePieChart.data.datasets[0].data = outcomeCategorieSums;
          outcomePieChart.data.labels = outcomeCategories;
          outcomePieChart.update()
      }
    }
    // Function to handle filter button clicks

    async function getMetaData() {
        const response = await fetch('/getMetaData');
        const data = await response.json();
        return data;
      }
      
      async function getFilteredData(selectedCategories, selectedMonths) {
        const url = '/getFilteredData';
        try {
          const response = await fetch(url, { method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({ time_filter:  selectedCategories, category_filter: selectedMonths })});
          if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
          }
          json = await response.json();
          console.log('Filtered data : ', json);
          console.log('Type : ', typeof json);
          // const categories_data = JSON.parse(json.categories);
          // const months_data = JSON.parse(json.months);
          // const categories = Object.keys(categories_data);
          // const categorie_sums = categories.map(category => categories_data[category]);
          // const months = Object.keys(months_data);
          // const month_sums = months.map(month => months_data[month]);
          // return { categories: categories, categorie_sums: categorie_sums , months : months, month_sums : month_sums};
          return json
        } catch (error) {
          console.error('Error fetching or parsing data:', error);
          return { categories: [], sums: [] , categorie_sums : [], months, month_sums : []};
        }
      }
    
      function jsonToList(json) {
        if (typeof json !== 'object' || json === null) {
          return { keys: [], values: [] }; // Handle non-object inputs
        }
      
        const keys = Object.keys(json);
        const values = keys.map(key => json[key]);
      
        return { keys, values };
      }

      init();
    });