var university;
$(document).ready(function() {
    var str = window.location.href;
    var n = str.lastIndexOf('/');
    university = Number(str.substring(n + 1));
    $("#rateYo").rateYo({
      rating: parseFloat($('.rating').text()),
      readOnly: true
    });
});

$(".school").click(function() {
    $('.type').empty().append("Subject");
    var school = $(this).text();

        $.post('/school-details',{ 
            university: university,
            school:school,
            what:"query-subjects",
            csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value
        },function(data) {
            data = data.courses;
            $('.pick-course').empty();
            var htmlstr="";
            for (var i in data) {
                htmlstr +='<button class="btn btn-teal full course"><h3>'+data[i]+'</h3></button>';
            }
            $('.pick-course').append(htmlstr);            
            $('.pick-course').css({
                'max-height':'500px',
                'overflow-y':'scroll',
                'overflow-wrap':'break-word',
            });

            $('.pick-course button').css({
                'white-space':'normal'
            });

            $('.course').click(function() {
                if($(this).text()=="") {
                    return;
                }
                course = $(this).text();
                $.post('/school-details',{ 
                    university: university,
                    school:school,
                    course:course,
                    what:"course-selected",
                    csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value
                },function(data) {
                    window.location.replace("/review-course/"+data.id);
            });
        });

    });
});

$('.btn-add-comment').click(function() {
    var textarea_styling= "<textarea id='text' style='width:100%;height:200px;padding:2%;font-family: 'Abel', sans-serif; \
     line-height: 25px;border: solid 1px #ddd;'></textarea><br>\
     <span> Add a rating </span> <br>\
     <label class='radio-inline'><input type='radio' name='rateRadio' value='1'>1</label>\
    <label class='radio-inline'><input type='radio' name='rateRadio' value='2'>2</label>\
    <label class='radio-inline'><input type='radio' name='rateRadio' value='3'>3</label>\
    <label class='radio-inline'><input type='radio' name='rateRadio' value='4'>4</label>\
    <label class='radio-inline'><input type='radio' name='rateRadio' value='5'>5</label>";

	swal({
        title: "Add Your Honest Opinion",
        text: textarea_styling,
        html: true,
        showCancelButton: true,
        closeOnConfirm: false,
        showLoaderOnConfirm: true,
        animation: "slide-from-top",
     }, function() {
        var review = document.getElementById('text').value;

        var rating = Number($("input[name='rateRadio']:checked").val());

        $.post('/add-review', {
            what:"university",
            university: university,
            review: review,
            rating: rating,
            csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
            },function(data) {            
            if (data == "Success") {
                swal.close();
                location.reload();
            } else {
                swal("Error!", "The review could not be added", "error");                
            }
        }, location.reload());
    });
});


$(".rateYo").each(function() {
	
	var item = $(this)

    item.rateYo({
		rating: item.data('id')
    });
});


function initMap() {
    var lat = parseFloat($('.map-lat').val());
    var lng = parseFloat($('.map-lng').val());
    var zoom = 16;
    if(lat == 0.0) {
        zoom = 4;
        lat = 51.5074;
        lng = 0.1278;
    }
    var uluru = {lat: lat, lng: lng};
    var map = new google.maps.Map(document.getElementById('map'), {
        zoom: zoom,
        center: uluru
    });
    var marker = new google.maps.Marker({
        position: uluru,
        map: map
    });
}