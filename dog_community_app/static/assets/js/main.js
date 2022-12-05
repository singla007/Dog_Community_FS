(function ($) {
    "use strict";

    // Spinner
    var spinner = function () {
        setTimeout(function () {
            if ($('#spinner').length > 0) {
                $('#spinner').removeClass('show');
            }
        }, 1);
    };
    spinner();
    
    
    // Initiate the wowjs
    new WOW().init();
    // $(function () {
    //     $.ajaxSetup({
    //         headers: {
    //             "X-CSRFToken": getCookie("csrftoken")
    //         }
    //     });
    // });
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    // Fixed Navbar
    $(window).scroll(function () {
        if ($(window).width() < 992) {
            if ($(this).scrollTop() > 45) {
                $('.fixed-top').addClass('bg-dark shadow');
            } else {
                $('.fixed-top').removeClass('bg-dark shadow');
            }
        } else {
            if ($(this).scrollTop() > 45) {
                $('.fixed-top').addClass('bg-dark shadow').css('top', -45);
            } else {
                $('.fixed-top').removeClass('bg-dark shadow').css('top', 0);
            }
        }
    });
    
    // Back to top button
    $(window).scroll(function () {
        if ($(this).scrollTop() > 300) {
            $('.back-to-top').fadeIn('slow');
        } else {
            $('.back-to-top').fadeOut('slow');
        }
    });
    $('.back-to-top').click(function () {
        $('html, body').animate({scrollTop: 0}, 1500, 'easeInOutExpo');
        return false;
    });
    $("#scrollToMain").click(function() {
        window.scrollTo({
            behavior: 'smooth',
            top:
                document.getElementById("main-section").getBoundingClientRect().top -
                document.body.getBoundingClientRect().top -
                80,
        }) 
        
    });

    $("#find-breed").click(function( event ) {
        event.preventDefault();
        var breed_info_title = $("input[name=breed-info]").val()
        window.scrollTo({
            behavior: 'smooth',
            top:
              document.getElementById(breed_info_title).getBoundingClientRect().top -
              document.body.getBoundingClientRect().top -
              90,
          })   
    })
    $.fn.adoptButton = function() {
        var dog_q = $(this).attr("data-dog-id")
        filterDogsByDog($(this), dog_q)
    }
    
    function filterDogsByBreed(that, breed){
        var token = $("input[name=csrfmiddlewaretoken]").val()
        // Stop form from submitting normally
        // Get some values from elements on the page:
        var $select = that,
            breed_id = breed,
            action_taken = breed_id>0 ?'filter_dogs': 'featured_dogs',
            url = $select.attr( "action" ) + "/list"
        // Send the data using post
        $.ajax({
            url: url,
            data: {
                action: action_taken, 
                breed_id: breed_id,
                CSRF: token
            },
            headers: {
                "X-CSRFToken" : token
            },
            method:'POST',
            success: function( data ) {
                var adoption_list_element = $('<div />').append(data).find("#adoption-list").html()
                console.log(adoption_list_element)
                $('#adoption-list').html(adoption_list_element);
                if(breed_id>0){
                    $('#featured-dogs-text').html('');
                }
                else{
                    $('#featured-dogs-text').html('Featured Dogs');
                }
            },
            error: function (request, status, error) {
                console.log(request.responseText);
            }
        })
    }

    function filterDogsByDog(that, dogId){
        var token = $("input[name=csrfmiddlewaretoken]").val()
        $("#adopt-form").modal('show')

        // Send the data using post
        $.ajax({
            url: $(that).attr("data-url")+ "/list",
            data: {
                action: "get_dog_data",
                dog_id: dogId,
                CSRF: token
            },
            headers: {
                "X-CSRFToken" : token
            },
            method:'POST',
            success: function( data ) {
                $("#id_dog_name").val(data.dogName)
            }
        })
    }
    
    $( "#filter-by-breed").on('change',function( event ) {
        event.preventDefault();
        var breed_id = $(this).val()
        filterDogsByBreed($(this), breed_id)
    });

    $( "#search-breed-button").click(function( event ) {
        event.preventDefault();
        var token = $("input[name=csrfmiddlewaretoken]").val()
        var url = $(this).attr( "action" ) + "/list"
        var breed = $("input[name=breed]").val()
        
        $.ajax({
            url: url,
            data: {
                action: 'breed_name_to_breed_id', 
                breed_name: breed,
                CSRF: token
            },
            headers: {
                "X-CSRFToken" : token
            },
            method:'POST',
            success: function( data ) {
                $("#filter-by-breed").val(data.breed_id);
                $("#filter-by-breed").change();

            }
        })
        window.scrollTo({
            behavior: 'smooth',
            top:
                document.getElementById("adoption-list").getBoundingClientRect().top -
                document.body.getBoundingClientRect().top -
                90,
        }) 
        
    });

    // meetup
    $.fn.meetUpBook = function() {
        var event_id_q = $(this).attr("data-event-id")
        $("#meetup-form").modal('show')
        $("#event_id").val(event_id_q)
    }

//    $("#formSuccess").addEventListener('change', function(event) {
//         event.target.val("test")
//    })
    $.fn.meetUpContact = function() {
        var event_q = $(this).attr("data-event")
        var event_time = $(this).attr("data-event-time")
        const message = `I would like to know more about the dog meetup event organised at ${event_q.location} starfing from ${event_time} for ${event_q.event_duration} hours.`
        // location.assign(window.location.origin + `/home#contact-us?contactmessage=${message}`)
        location.assign(window.location.origin + `/home#contact-us`)
    }

    $.fn.formSuccess = function(id, action, data, user_email,user_name) {
        console.log(id,action,data, user_email)
        // sending email to the user for confirmation
        // data: {
        //     "email" : `${user_email}`,
            // "email_description": `Hello,\n \
            //     Hope you are doing well! Thank you for registering for this meetup. Please be polite and courteous with other while enjoying with your dogs. Also, please take care of safety and cleanliness.\n \
            //     Park Location - ${data.event_location}\n \
            //     Starts at - ${data.event_time} \n \
            //     Duration - ${data.event_duration} hours \n \
            //     Hope to see you there! \n \n \
            //     Thanks and Regards\n \
            //     Dogs Community`,
        //     "email_subject": `Community meet at ${data.event_location}`
        // },
        var mailBody = {
            "email": `${user_email}`,
            "email_description": "demo-test",
            "email_subject": "demo-subject Dog Community"
        }
        if (action == 'meetup'){
            mailBody['email_description'] =  `Hello ${user_name},\n 
                Hope you are doing well! Thank you for registering for this meetup. Please be polite and courteous with other while enjoying with your dogs. Also, please take care of safety and cleanliness.\n
                Park Location - ${data.event_location}\n 
                Starts at - ${data.event_time} \n 
                Duration - ${data.event_duration} hours \n 
                Hope to see you there! \n \n 
                Thanks and Regards\n 
                Dogs Community`;
            mailBody['email_subject'] = `Community meetup at ${data.event_location}`
            
        }
        if (action == 'adoption'){
            mailBody['email_description'] =  `Hello ${user_name},\n 

                Hope you are doing well! Thank you for taking this intiative. \n

                Adoption details: \n
                Dog's name - ${data.dog_name}\n 
                Dog's Age - ${data.dog_age} years \n 
                Dog's color - ${data.dog_color} hours \n 
                
                Our representative will call you in next few days for next steps \n

                Thanks and Regards\n 
                Dogs Community\n
                Phone Number: +1 555 454 1345\n
                Address: 20 Knoxdale Crescent, K17 A5T`;
            mailBody['email_subject'] = `Adoption for ${data.dog_name}`
        }
        if (action == 'report-missing'){
            console.log("missing dog")
            mailBody['email_description'] =  `Hello ${user_name},\n 

                Hope you are doing well! Thank you for taking this intiative. \n
                We acknowledge that we have received this email. 

                Missing dog details: \n
                Dog's name - ${data.dog_name}\n 
                Dog's Age - ${data.dog_age} years \n 
                Dog's color - ${data.dog_color} \n 
                Dog details - ${data.unique_identification} \n
                Last known location - ${data.dog_last_location}\n
                
                Our representative will call you in next few days for next steps \n

                Thanks and Regards\n 
                Dogs Community\n
                Phone Number: +1 555 454 1345\n
                Address: 20 Knoxdale Crescent, K17 A5T`
            mailBody['email_subject'] = `Missing dog from ${data.dog_last_location}`
        }

        if (action == 'report-stray'){
            mailBody['email_description'] =  `Hello ${user_name},\n 

                Hope you are doing well! Thank you for taking this intiative. \n
                We acknowledge that we have received this email. 
                
                Rescued dog details: \n
                Dog's name - ${data.dog_name}\n 
                Dog's Age - ${data.dog_age} years\n 
                Dog's color - ${data.dog_color} \n 
                Dog details - ${data.unique_identification} \n
                Rescued from - ${data.dog_last_location}\n
                
                Our representative will call you in next few days for next steps \n

                Thanks and Regards\n 
                Dogs Community\n
                Phone Number: +1 555 454 1345\n
                Address: 20 Knoxdale Crescent, K17 A5T`
            mailBody['email_subject'] = `Rescued dog from ${data.event_location}`
        }
        var url = 'https://prod-12.canadacentral.logic.azure.com:443/workflows/83e44d334b814c69a103323e596dd428/triggers/manual/paths/invoke?api-version=2016-10-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=VmVmf4Q-slQQW7i2sibJUhw4-fblPmmHBZ-mAAHYgNg'
        $.ajax({
            url: url,
            data: JSON.stringify(mailBody),
            method:'POST',
            contentType: 'application/json',
            success: function( data ) {
                console.log(data + "success")
            },
            error: function (request, status, error) {
                console.log(request.responseText);
            }
        })
    }

})(jQuery);

