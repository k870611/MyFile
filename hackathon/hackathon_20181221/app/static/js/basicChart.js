var basicChart = {
	version: "0.0.1"
}

! function(){
	"use strict";
	
	basicChart.getVersion = function(){
		return basicChart.version;
	};
	
	basicChart.valueParse = function(s){
		var str = s.toString();
		var value = 0;
		var arr = []
		
		if(str.startsWith('0x')){
			value = parseInt(str, 16);
			
		}else{
			var reg = /\d+.?(\d+)?/;
			arr = str.match(reg);
			
			try{
				value = parseFloat(arr[0]);
				
			}catch(err){
				value = -1
			}
		}
		
		if(value == null){
			value = -1;
		}
		
		return value;
	};
	
	basicChart.drawLinebyNVD3 = function(s, data){
		s.html(null);
		d3.selectAll('.nvtooltip').remove();
		nv.addGraph(function() {
		    var chart = nv.models.lineChart();
		    
		    chart.useInteractiveGuideline(true);
		    chart.color(d3.scale.category20().range());

	    	chart.xAxis.rotateLabels(-15).tickFormat(function(d) {
	    		return d;
	     	});

		    chart.yAxis.tickFormat(d3.format(',.2f'));

		    s.datum(data).call(chart);

		    nv.utils.windowResize(function(){
		    	d3.selectAll('svg > *').remove();
		    	chart.update();
		    });

		    return chart;
		});		
	};
	
	basicChart.drawBarbyNVD3 = function(s, data){
		s.html(null);
		d3.selectAll('.nvtooltip').remove();
		nv.addGraph(function() {
			
		    var chart = nv.models.multiBarChart().stacked(true);	    
		    chart.color(d3.scale.category20().range());
	
	    	chart.xAxis.tickFormat(function(d) {
	    		return d;
	     	});
	
		    chart.yAxis.tickFormat(d3.format(',.2f'));		    
	
		    s.datum(data).transition().duration(0).call(chart);
	
		    nv.utils.windowResize(function(){
		    	d3.selectAll('svg > *').remove();
		    	chart.update();
		    });
	
		    return chart;
		});		
	}
	
	basicChart.drawStackbyNVD3 = function(s, data){
		s.html(null);
		d3.selectAll('.nvtooltip').remove();
		if(data == null){
			return;
		}
		
		nv.addGraph(function() {
			//var w = s[0][0].clientWidth;

			var chart = nv.models.stackedAreaWithFocusChart()
            .useInteractiveGuideline(true)
            .x(function(d) { if(d != undefined) return d.x})
            .y(function(d) { return d.y })
            .controlLabels({stacked: "Stacked"})
            .duration(300);
			
			chart.color(d3.scale.category20().range());

			var startTime = data[0].values[0].x;
			var endTime = data[0].values[data[0].values.length-1].x
			
	        chart.brushExtent([startTime, endTime]);
			
	
	        chart.xAxis.ticks(5).tickFormat(function(d) { return d});
	        chart.x2Axis.ticks(5).tickFormat(function(d) { return d });
	        chart.yAxis.tickFormat(d3.format(',.2f'));
	        chart.y2Axis.tickFormat(d3.format(',.2f'));
	
	        chart.legend.vers('furious');
	
	        s.datum(data)
	        	.transition().duration(1000)
	            .call(chart)
	            .each('start', function() {
	                setTimeout(function() {
	                    s.selectAll('*').each(function() {
	                        if(this.__transition__)
	                            this.__transition__.duration = 1;
	                    })
	                }, 0)
	            });
	
	        nv.utils.windowResize(function(){
		    	d3.selectAll('svg > *').remove();	    	
		    	chart.update();
		    });
	        
	        return chart;
		});		
	}
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
}();



