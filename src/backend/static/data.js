color_palette = {
  'incomes' : ['#d8f3dc', '#b7e4c7', '#95d5b2', '#74c69d', '#52b788', '#40916c', '#2d6a4f', '#1b4332', '#081c15'], 
  // 'incomes' : ["#03045e","#023e8a","#0077b6","#0096c7","#00b4d8","#48cae4","#90e0ef","#ade8f4","#caf0f8"], 
  'outcomes' : ['#ffba08', '#faa307', '#f48c06', '#e85d04', '#e85d04', '#dc2f02', '#d00000', '#9d0208', '#6a040f', '#370617', '#03071e'],
  'outcomes_references' : ['#ffba08', '#d00000', '#6a040f']
}

function concat_uniques(array1, array2){
  return array1.concat(array2).filter((v,i,a)=>a.indexOf(v)==i)
}
/**
 * Generates an array of progressive shades of color, interpolating between three reference colors
 * with customizable proportions for each interpolation segment.
 *
 * @param {number} length The desired length of the array (number of shades).
 * @param {string} startColor The starting color in hexadecimal format (e.g., "#FFFF00" - Yellow).
 * @param {string} middleColor The middle color in hexadecimal format (e.g., "#FF0000" - Red).
 * @param {string} endColor The ending color in hexadecimal format (e.g., "#000000" - Black).
 * @param {number} [proportion=0.5] The proportion of colors to use in the first segment
 * (between startColor and middleColor). Must be between 0 and 1.
 * The remaining proportion will be used for the second segment
 * (between middleColor and endColor). Defaults to 0.5 (even split).
 * @returns {string[]} An array of strings, where each string is a hexadecimal color code
 * representing a shade, interpolating between the start, middle, and end colors.
 * Returns an empty array if the input length is not a positive integer, if any color is invalid,
 * or if the proportion is not a valid number between 0 and 1.
 */
function generateShades(length, startColor, middleColor, endColor, proportion = 0.5) {
  if (typeof length !== 'number' || length <= 0 || !Number.isInteger(length)) {
    return [];
  }

  if (typeof proportion !== 'number' || proportion < 0 || proportion > 1) {
    console.error("Error: 'proportion' must be a number between 0 and 1.");
    return [];
  }

  const hexToRgb = (hex) => {
    if (!/^#([0-9A-Fa-f]{3}){1,2}$/.test(hex)) {
      return null;
    }
    const hexValue = hex.substring(1);
    const bigint = parseInt(hexValue, 16);
    const r = (bigint >> 16) & 255;
    const g = (bigint >> 8) & 255;
    const b = bigint & 255;
    return { r, g, b };
  };

  const startRgb = hexToRgb(startColor);
  const middleRgb = hexToRgb(middleColor);
  const endRgb = hexToRgb(endColor);

  if (!startRgb || !middleRgb || !endRgb) {
    return []; // Invalid color format
  }

  const shades = [];
  const firstSegmentLength = Math.floor(length * proportion);
  const secondSegmentLength = length - firstSegmentLength;

  for (let i = 0; i < length; i++) {
    let r, g, b;

    if (i < firstSegmentLength) {
      // Interpolate between startColor and middleColor
      const factor = i / (firstSegmentLength - 1 || 1);
      r = Math.round(startRgb.r + (middleRgb.r - startRgb.r) * factor);
      g = Math.round(startRgb.g + (middleRgb.g - startRgb.g) * factor);
      b = Math.round(startRgb.b + (middleRgb.b - startRgb.b) * factor);
    } else {
      // Interpolate between middleColor and endColor
      const indexInSecondSegment = i - firstSegmentLength;
      const factor = indexInSecondSegment / (secondSegmentLength - 1 || 1);
      r = Math.round(middleRgb.r + (endRgb.r - middleRgb.r) * factor);
      g = Math.round(middleRgb.g + (endRgb.g - middleRgb.g) * factor);
      b = Math.round(middleRgb.b + (endRgb.b - middleRgb.b) * factor);
    }

    const hexR = r.toString(16).padStart(2, '0');
    const hexG = g.toString(16).padStart(2, '0');
    const hexB = b.toString(16).padStart(2, '0');
    shades.push(`#${hexR}${hexG}${hexB}`);
  }

  return shades;
}
/**
 *  Return a sorted array of the colors based on the values.
 * @param {*} colors 
 * @param {*} values 
 * @returns 
 */
function sortColorsByValues(colors, values) {
  
  if (colors.length !== values.length) {
    console.error("Error: The 'colors' and 'values' arrays must have the same length.");
    return [];
  }
  const valuePairs = colors.map((color, index) => ({
    color: color,
    value: values[index],
    index: index
  }));
  valuePairs.sort((a, b) => a.value - b.value);
  const colorPairs = valuePairs.map((elmt, index) => ({
    color: colors[index],
    index: elmt.index
  }))
  colorPairs.sort((a, b) => a.index - b.index);
  const sortedColors = colorPairs.map((pair) => pair.color);
  return sortedColors;
};

async function getFilteredData(selectedCategories, selectedMonths) {
  const url = '/getFilteredData';
  try {
    const response = await fetch(url, { method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ time_filter:  selectedMonths, category_filter: selectedCategories })});
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    json = await response.json();
    return json
  } catch (error) {
    console.error('Error fetching or parsing data:', error);
    return { categories: [], sums: [] , categorie_sums : [], months, month_sums : []};
  }
}

async function getMetaData() {
  const response = await fetch('/getMetaData');
  const data = await response.json();
  return data;
}

function jsonToList(json) {
  if (typeof json !== 'object' || json === null) {
    return { keys: [], values: [] }; // Handle non-object inputs
  }

  const keys = Object.keys(json);
  const values = keys.map(key => json[key]);

  return { keys, values };
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
        labels: [],
        datasets: [{
          label: 'Total Expenses Over Time',
          data: [],
          borderColor: 'rgb(75, 192, 192)',
          tension: 0.1,
          backgroundColor: []
        }]
      };
      const outcomePieChartData = {
        labels: [],
        datasets: [{
          label: 'Expenses by Category',
          data: [],
          backgroundColor: [],
          hoverOffset: 4
        }]
      };
          
      // Get chart contexts
      const incomeTimeSeriesCtx = document.getElementById('incomeTimeSeriesChart').getContext('2d');
      const incomePieChartCtx = document.getElementById('incomePieChart').getContext('2d');
      const outcomeTimeSeriesCtx = document.getElementById('outcomeTimeSeriesChart').getContext('2d');
      const outcomePieChartCtx = document.getElementById('outcomePieChart').getContext('2d');
      
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

  
      createFilterButtons(availableCategories, categoryFiltersContainer, 'category');
      createFilterButtons(availableMonths, monthFiltersContainer, 'month');
      
      updateChartsWithFilteredData(['*'], ['*'])
  
      // --- Chart Update with Filtered Data ---
      async function updateChartsWithFilteredData(selectedCategories, selectedMonths) {
          const data = await getFilteredData(selectedCategories, selectedMonths)
          const incomeCategories = data.incomes.categories;
          const incomeCategorieSums = data.incomes.categorie_sums;
          const incomeMonths = data.incomes.months;
          const incomeMonthSums = data.incomes.month_sums;
          let outcomeCategories = data.outcomes.categories;
          let outcomeCategorieSums = data.outcomes.categorie_sums;
          let outcomeMonths = data.outcomes.months;
          let outcomeMonthSums = data.outcomes.month_sums;
          // updateSankai(incomeCategories, incomeCategorieSums, outcomeCategories, outcomeCategorieSums);
          
          mix_sums = outcomeCategories.map((category, index) => ({
            category : category,
            sum : outcomeCategorieSums[index]
          }))
          mix_sums.sort((a, b) => a.sum - b.sum)
          outcomeCategories = mix_sums.map((a) => a.category)
          outcomeCategorieSums = mix_sums.map((a) => a.sum)
          const incomeTimeSeriesColors = sortColorsByValues(color_palette.incomes.slice(0, incomeMonthSums.length), incomeMonthSums)
          const incomeCategoriesColors = sortColorsByValues(color_palette.incomes.slice(0, incomeCategorieSums.length), incomeCategorieSums)
          incomeTimeSeriesChart.data.datasets[0].data = incomeMonthSums;
          incomeTimeSeriesChart.data.labels = incomeMonths;
          incomeTimeSeriesChart.data.datasets[0].backgroundColor = incomeTimeSeriesColors;
          incomeTimeSeriesChart.update()
          incomePieChart.data.datasets[0].data = incomeCategorieSums;
          incomePieChart.data.datasets[0].backgroundColor = incomeCategoriesColors;
          incomePieChart.data.labels = incomeCategories;
          incomePieChart.update()

          
          const outcomeTimeSeriesColors = sortColorsByValues(generateShades(outcomeMonthSums.length, color_palette.outcomes_references[0], color_palette.outcomes_references[1], color_palette.outcomes_references[2], 0.9), outcomeMonthSums)
          const outcomeCategoriesColors = sortColorsByValues(generateShades(outcomeCategorieSums.length, color_palette.outcomes_references[0], color_palette.outcomes_references[1], color_palette.outcomes_references[2], 0.9), outcomeCategorieSums)
          outcomeTimeSeriesChart.data.datasets[0].data = outcomeMonthSums;
          outcomeTimeSeriesChart.data.datasets[0].backgroundColor = outcomeTimeSeriesColors;
          outcomeTimeSeriesChart.data.labels = outcomeMonths;
          outcomeTimeSeriesChart.update()
          outcomePieChart.data.datasets[0].data = outcomeCategorieSums;
          outcomePieChart.data.datasets[0].backgroundColor = outcomeCategoriesColors;
          outcomePieChart.data.labels = outcomeCategories;
          outcomePieChart.update()
      }

    // Function to handle filter button clicks
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
      
      function handleFilterButtonClick(event) {
              
        const button = event.target;
        button.classList.toggle('active'); // Toggle active class for visual feedback
      
        const selectedCategories = Array.from(categoryFiltersContainer.querySelectorAll('button.active'))
            .map(btn => btn.dataset.filterValue);
        const selectedMonths = Array.from(monthFiltersContainer.querySelectorAll('button.active'))
            .map(btn => btn.dataset.filterValue);
      
      
        updateChartsWithFilteredData(selectedCategories, selectedMonths);
      }

    }
      init();
    });
// google.charts.load('current', {'packages':['sankey']});
// google.charts.setOnLoadCallback(drawChart);



// function updateSankai(incomeCategories, incomeCategorieSums, outcomeCategories, outcomeCategorieSums) {
//   var data = new google.visualization.DataTable();
//   var rows = []
//   data.addColumn('string', 'From');
//   data.addColumn('string', 'To');
//   data.addColumn('number', 'Weight');
//   data.addRows([
//     [ 'A', 'X', 5 ],
//     [ 'A', 'Y', 7 ],
//     [ 'A', 'Z', 6 ],
//     [ 'B', 'X', 2 ],
//     [ 'B', 'Y', 9 ],
//     [ 'B', 'Z', 4 ]
//   ]);

//   // Sets chart options.
//   var options = {
//     width: 600,
//   };

//   // Instantiates and draws our chart, passing in some options.
//   var chart = new google.visualization.Sankey(document.getElementById('sankey_basic'));
//   chart.draw(data, options);
// }