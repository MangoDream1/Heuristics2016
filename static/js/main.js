function getJson() {
	var id =getUrlParameter("id");

	$.getJSON("/json", data={"id": id}, function(json) {
		console.log(json);
		if (json.results == "Error") {
			// Doe iets hier voor error
		} else {

			// Transpose json object from column to row order
			var timetable = {};
			$.each(json, function(i, day){
				$.each(day, function(z, timeslot){

					if (timetable[z]) {
						timetable[z].push(timeslot)
					} else {
						timetable[z] = [timeslot];
					}
				});
			});

			var table = $("<table></table>")

			DAYS = {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday",
			        4: "Friday", 5: "Saturday", 6: "Sunday"}
			TIMESLOTS = {0: "9-11", 1: "11-13", 2: "13-15", 3: "15-17", 4: "17-19"}

			// Adds days of week
			var row = $("<tr></tr>");
			row.append($("<th></th>").text(""));
			for (i=0; i<timetable["0"].length; i++) {
				row.append($("<th></th").text(DAYS[i]));
			}

			table.append(row);

			// Adds the data to table
			$.each(timetable, function(i, timeslot){
				var row = $("<tr></tr>");
				row.append($("<th></th").text(TIMESLOTS[i]));

				$.each(timeslot, function(i, day){
					var column = $("<th></th>").text("");
					$.each(day, function(i, lecture){
						column = $("<th></th>").append(lecture.subject + "<br>" + lecture.classroom + "<br>" + lecture.string);
					})

					if ($(day).length > 1) {
						column.css("background-color", "red");
						column.css("font-size", "35px");
						column.css("color", "black");
						column.text($(day).length);

						$.each(day, function(i, lecture){
							$('#'+lecture.string).css("background-color", "red").css("color", "black");
						})
					}


					row.append(column)
				})

				table.append(row);
			})

			$('#timetable').append(table);
		}
	});

}

// Copied from:
// http://stackoverflow.com/questions/19491336/get-url-parameter-jquery-or-how-to-get-query-string-values-in-js#21903119
var getUrlParameter = function getUrlParameter(sParam) {
    var sPageURL = decodeURIComponent(window.location.search.substring(1)),
        sURLVariables = sPageURL.split('&'),
        sParameterName,
        i;

    for (i = 0; i < sURLVariables.length; i++) {
        sParameterName = sURLVariables[i].split('=');

        if (sParameterName[0] === sParam) {
            return sParameterName[1] === undefined ? true : sParameterName[1];
        }
    }
};

getJson();
