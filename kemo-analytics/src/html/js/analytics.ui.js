function customTooltipsLabel(tooltipItem, data) {
    var data_item = stats_data[tooltipItem.index];
    return [
            "User: " + data_item.user_stat.user_count + " ( '/' "+data_item.user_stat.index_count+", '/chat' "+data_item.user_stat.chat_count+")",
            "From blog: " + data_item.user_stat.from_blog_count,
            "Robots: " + data_item.robot_count,
            "Hacks: " + data_item.hack_count,
            "All: " + data_item.all_count
            ];
}

function toChartLabels(stats_data){
    var labels = [];
    for(key in stats_data){
        labels.push(stats_data[key].day);
    }
    return labels;
}

function toChartValues(stats_data){
    var values = [];
    for(key in stats_data){
        values.push(stats_data[key].user_stat.user_count);
    }
    return values;
}


var ctx = document.getElementById("accessLogChart");
var chart = new Chart(ctx, {
    defaultFontColor: 'white',
    type: 'line',
    data: {
        labels: toChartLabels(stats_data),
        datasets: [{
            label: '# of Requests',
            data: toChartValues(stats_data),
            backgroundColor: 'rgba(255, 99, 132, 0.2)',
            borderColor: 'hotpink',
            borderWidth: 2
        }]
    },
    options: {
        scaleFontColor: "#FFFFFF",
        scales: {
            yAxes: [{
                gridLines : {
                    color: 'rgba(255, 255, 255, 0.2)'
                },
                ticks: {
                    beginAtZero:true,
                    fontColor: 'white'
                }
            }],
            xAxes: [{
                gridLines : {
                    color: 'rgba(255, 255, 255, 0.2)'
                },
                ticks: {
                    beginAtZero:true,
                    fontColor: 'white'
                }
            }],
        },
        tooltips: {
            enabled: true,
            callbacks: {
                label: customTooltipsLabel
              }
         },
         legend: {
            display: true,
            labels: {
                fontColor: 'white'
            }
        }
    }
});

(function(){

    aui.onElement("last_requests_tbody", function(tbody){
        for(var key in last_requests){
            var record = last_requests[key];
            tbody.appendChild(aui.tr([record[0],record[1],record[2],record[3],record[8]]));
        }
    });

    aui.onElement("user_agents", function(tbody){
        for(var key in user_agents){
            tbody.appendChild(aui.tr([user_agents[key]]));
        }
    });

user_agents

})();
