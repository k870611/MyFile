// Get data-----------------------------------------------------------------------------
d3.json("/data/temp_data", function(data) {
	$('#checkboxes').html(null);
	total_data_set = data;
});

var total_data_set = {};
$('#tb_table').hide();

// table click-----------------------------------------------------------------------------
$('#btnTable').click(function(){
    var json_info = total_data_set;
    $('#tb_table tbody').html(null).scrollTop(0);

    console.log(json_info)

    for(var idx in json_info){

        var date = json_info[idx]["time"];
        var value = json_info[idx]["value"] + " °C";

        $('#tb_table tbody').append("<tr><td>"+
            date +"</td><td>"+
            value +"</td></tr>");
    }

    $('#tb_table').show();
    $('#s').hide();
});

// Line Chart-----------------------------------------------------------------------------
$('#btnLine').click(function(){
    $('#tb_table').hide();
    $('#s').show();
    DrawChart("line");
});

// Bar Chart-----------------------------------------------------------------------------
$('#btnBar').click(function(){
    $('#tb_table').hide();
    $('#s').show();
    DrawChart("bar");
});

// Stack Chart-------------------------------------------------------------------------------
$('#btnStack').click(function(){
    $('#tb_table').hide();
    $('#s').show();
    DrawChart("stack");
});

$('#btnPredict').click(function(){
    $("#Loading").show();
    $("#predict_output").html("Predicting, please wait ~~~~");
	$("#predict_output").show();

    $.ajax({
        type: "POST",
        url: $SCRIPT_ROOT + "/weather_predict",
        cache: false,
        success: function(data) {
            var overheat_date = data.temp;

            $("#predict_output").html("Overheat date( > 60°C) : " + overheat_date);
            $("#predict_output").show();
			$('#Loading').hide();
        },
        error: function(xhr, ajaxOptions, thrownError) {
            console.log('error');
            $('#Loading').hide();
        }
    });
});

//DrawChart----------------------------------------------------
function DrawChart(chart){
    var chart_data = [];

    var json_info = total_data_set;
	var data = [];
	console.log(json_info);

	for(var idx in json_info){
		var myDate =  new Date(json_info[idx].time).getTime();
		var myValue =json_info[idx]["value"];

		data.push({x:myDate, y:myValue});
	}

	d3.selectAll('svg > *').remove();
	var s = d3.select('#s');
	chart_data.push({values: data, key: "Server Temp"});

	if(chart == "line"){
	    $("#predict_output").hide();
		basicChart.drawLinebyNVD3(s, chart_data);

	}else if(chart == "bar"){
	    $("#predict_output").hide();
		basicChart.drawBarbyNVD3(s, chart_data);

	}else if(chart == "stack"){
	    $("#predict_output").show();
	    $("#predict_output").html("Can not show stack chart (data set < 1) ");
	    return;
		// basicChart.drawStackbyNVD3(s, chart_data);
	}
}