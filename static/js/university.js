var university;
$(document).ready(function() {
    var str = window.location.href;
    var n = str.lastIndexOf('/');
    university = Number(str.substring(n + 1));
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

$(function () {
    $("#rateYo").rateYo({
      rating: Number($('.rating').text())
    });
});

function initMap() {
    var uluru = {lat: 55.87212109999999, lng: -4.288200500000016};
    var map = new google.maps.Map(document.getElementById('map'), {
        zoom: 16,
        center: uluru
    });
    var marker = new google.maps.Marker({
        position: uluru,
        map: map
    });
}