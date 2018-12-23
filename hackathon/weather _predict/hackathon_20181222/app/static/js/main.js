var total_data_set = {};
$('#tb_table').hide();



// datepicker-----------------------------------------------------------------------------
var $weather_date = $('#weather_date').intimidatetime({
    format: 'yyyy-MM-dd',
    buttons:
        [{
            text: 'Done',
            action: function(e){ $weather_date.intimidatetime('close'); return false; }
        },
        {
            text: 'Now',
            action: function(e){ $weather_date.intimidatetime('value', new Date() ); return false; }
        }]
});

// table click-----------------------------------------------------------------------------
$('#btnTable').click(function(){
    get_checked_chk();
    if(aryCheckboxSelectX.length<=0){
        return;
    }

    var year = aryCheckboxSelectX[aryCheckboxSelectX.length-1];
    for(var data in total_data_set){
        if (total_data_set[data]["time"] == year){
            var temp_data = total_data_set[data]["value"];
            break;
        }
    }

    $('#tb_table tbody').html(null).scrollTop(0);

    for(var i in temp_data){
        var date = year + " / " + (parseInt(i)+1);
        var value = temp_data[i];

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

    get_checked_chk();

    if(aryCheckboxSelectX.length<=0){
        return;
    }

    DrawChart("line");
});

// Bar Chart-----------------------------------------------------------------------------
$('#btnBar').click(function(){
    $('#tb_table').hide();
    $('#s').show();

    get_checked_chk();
    if(aryCheckboxSelectX.length<=0){
        return;
    }

    DrawChart("bar");
});

// Stack Chart-------------------------------------------------------------------------------
$('#btnStack').click(function(){
    $('#tb_table').hide();
    $('#s').show();

    get_checked_chk();
    if(aryCheckboxSelectX.length<=0){
        return;
    }

    DrawChart("stack");
});

// Weather Predict-------------------------------------------------------------------------------
function isDateTime(dateTime)
{
    var dateTimeRegex=/^(?:(?!0000)[0-9]{4}-(?:(?:0[1-9]|1[0-2])-(?:0[1-9]|1[0-9]|2[0-8])|(?:0[13-9]|1[0-2])-(?:29|30)|(?:0[13578]|1[02])-31)|(?:[0-9]{2}(?:0[48]|[2468][048]|[13579][26])|(?:0[48]|[2468][048]|[13579][26])00)-02-29)\s*/;
    return dateTimeRegex.test(dateTime);
}

function input_check(input_obj, type){
    var val = input_obj.value;
    if(val == ""){
        return;
    }


    if(!isDateTime(val))
    {
        alert("格式错误");
        input_obj.value = "";
    }

}

$('#btnPredict').click(function(){
    var date_time = document.getElementById("weather_date").value;

    console.log(date_time);
    if(date_time == ""){
        return;
    }

    $.ajax({
        type: "POST",
        url: $SCRIPT_ROOT + "/weather_predict",
        data: {
            predict_date : date_time,
        },
        cache: false,
        success: function(data) {
            console.log(data.temp);

            degree = Math.round(data.temp * 100) / 100

            $("#predict_output").html("Temperature is : " + degree +" °C");
            $("#predict_output").show();

        },
        error: function(xhr, ajaxOptions, thrownError) {
            console.log('error');
            $('#Loading').hide();
        }
    });
});

$('#btnReCrawl').click(function(){
    $('#Loading').show();
    $("#predict_output").show();
    $("#predict_output").html("re-crawling, please wait ~~~~ ");

    $.ajax({
        type: "POST",
        url: $SCRIPT_ROOT + "/data_ReCrawl",
        cache: false,
        success: function(data) {
            if(data.info == "success"){
                $("#predict_output").html("Data is re-crawl !!! ");
            }else{
                $("#predict_output").html("re-crawl failure, please check proxy setting and resource website.");
            }

            $('#Loading').hide();
        },
        error: function(xhr, ajaxOptions, thrownError) {
            console.log('error');
            $('#Loading').hide();
        }
    });
});

//Multi Select----------------------------------------------------
var expanded = false;

function showCheckboxes() {
    var checkboxes = document.getElementById("checkboxes");

    if (!expanded) {
        checkboxes.style.display = "block";
        expanded = true;

    } else {
        checkboxes.style.display = "none";
        expanded = false;
    }
}

//Get checked chk----------------------------------------------------
var aryCheckboxSelectX = new Array();
function get_checked_chk() {
    var chk_box=$('.chk_year');
    aryCheckboxSelectX = new Array();

    for(var i=0;i<chk_box.length;i++){
        if(chk_box[i].checked){
            var chk_val = $('.chk_year:eq('+i+')').val();
            aryCheckboxSelectX.push(chk_val)
        }
    }
}

//DrawChart----------------------------------------------------
function DrawChart(chart){
    var chart_data = [];

    for(var c=0; c<aryCheckboxSelectX.length; c++){
        var year = aryCheckboxSelectX[c];

        for(var data in total_data_set){
            if (total_data_set[data]["time"] == year){
                var json_info = total_data_set[data];
                break;
            }
        }
        var data = [];

        for(var i=0; i<12; i++){
            json_info["value"]
            var myDate = (parseInt(i)+1);

            if(i < json_info["value"].length){
                var myValue =json_info["value"][i];

            }else{
                var myValue =0;
            }

            data.push({x:myDate, y:myValue});
        }

        d3.selectAll('svg > *').remove();
        var s = d3.select('#s');
        chart_data.push({values: data, key: year});

        if(c+1 == aryCheckboxSelectX.length && chart == "line"){
            basicChart.drawLinebyNVD3(s, chart_data);

        }else if(c+1 == aryCheckboxSelectX.length && chart == "bar"){
            basicChart.drawBarbyNVD3(s, chart_data);

        }else if(c+1 == aryCheckboxSelectX.length && chart == "stack"){
            basicChart.drawStackbyNVD3(s, chart_data);
        }
    }
}