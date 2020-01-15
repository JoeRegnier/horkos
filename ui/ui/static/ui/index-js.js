function add_reopen() {
    $('.status_btn').mouseenter(function () {
        if ($(this).hasClass('status_btn_active')) {
            $(this).text("Reopen");
        }
    });
    $('.status_btn').on('mouseleave', function () {
        if ($(this).hasClass('status_btn_active')) {
            if ($(this).hasClass('ignore')) {
                $(this).text("Ignored");
            }
            if ($(this).hasClass('verify')) {
                $(this).text("Verified");
            }
        }
    });
}

$(document).ready(function () {
    $('.close-details').on('click', function () {
        $('.details').addClass('hidden');
        $('#show-details-btn').addClass('disabled-show-details-btn');
    });
});

function build_query_details(query_selector) {
    var queries = JSON.parse(localStorage.queries).queries;
    var query = queries.filter(element => {
        return element.id == query_selector;
    })[0];
    $('#sql-query').text(query.querySql);
    $('#context-query').text(query.context_query);
    $('#scorethreshold_value').text(query.scoreThreshold.toFixed(0));
    $('#mostrecentrevision_value').text(query.mostRecentRevision);
    $('#lastruntime_value').text(query.most_recent_run_time.toFixed(2) + 's');
    $('#averageruntime_value').text(query.avg_run_time.toFixed(2) + 's');
    $('#numrecordedruns_value').text(query.num_recorded_runs);
    $('#databaseserver_value').text(query.database_server);
    $('#database_value').text(query.database);
    $('.statweights').remove();
    var staticweights = JSON.parse(localStorage.queries).staticweights;
    var stattechniques = JSON.parse(localStorage.queries).stattechniques;
    var query_weights = staticweights.filter(element => {
        return element.queryID_id == query_selector;
    });
    localStorage.query_weights = JSON.stringify(query_weights);
    var x = 0;
    for (var weight of query_weights) {
        stat_tech_name = stattechniques.filter(element => {
            return element.id == weight.statTechnique_id
        })[0];
        even_or_odd = (x % 2) == 0 ? 'even-row' : 'odd-row';
        row = '<div class="row statweights ' + even_or_odd + '" >' +
            '<div class="col-8">' +
            '<div class="row">' +
            '<b>' + stat_tech_name.statTechnique + ' </b>' +
            '</div>' +
            '</div>' +
            '<div class="col">' +
            '<div class="row justify-content-end">' +
            weight.weight +
            '</div>' +
            '</div>' +
            '</div>'
        x += 1;
        $('#weights_col').append(row);
    }
}

function add_button_implementation() {
    $('.status_btn').unbind('click').on('click', function () {
        var issue_change_state_url = './change_issue_state?id=' + $(this).attr('id').split('_')[1];
        if ($(this).hasClass('status_btn_active')) {
            issue_change_state_url += '&status=Open'
        } else {
            if ($(this).hasClass('verify')) {
                issue_change_state_url += '&status=Verified'
            }
            if ($(this).hasClass('ignore')) {
                issue_change_state_url += '&status=Ignored'
            }
        }
        $.ajax({
            url: issue_change_state_url,
            dataType: "json",
            success: function (data) {
                return;
            }
        });

        if ($(this).hasClass('status_btn_active')) {
            $(this).removeClass('status_btn_active');
            if ($(this).hasClass('ignore')) {
                $(this).text("Ignore");
            }
            if ($(this).hasClass('verify')) {
                $(this).text("Verfiy");
            }

        } else {
            $(this).addClass('status_btn_active');
            if ($(this).hasClass('ignore')) {
                $(this).text("Ignored");
                var other_button = $('#verify_' + $(this).attr('id').split('_')[1]);
                $(other_button).text('Verify');
                $(other_button).removeClass('status_btn_active');
            }
            if ($(this).hasClass('verify')) {
                $(this).text("Verified");
                var other_button = $('#ignore_' + $(this).attr('id').split('_')[1]);
                $(other_button).text('Ignore');
                $(other_button).removeClass('status_btn_active');
            }
        }
    });
}

function build_issue_list(selected_query) {
    var data = JSON.parse(localStorage.issues);
    $('.carousel_arrow').addClass('hidden-arrow');

    var issues = data.issues;
    if ($(".issues_carousel").hasClass('slick-initialized')) {
        $('.issues_carousel').slick('unslick');
    }

    $(".issue").remove();
    $(".issues_carousel").css({
        'display': 'None'
    });

    build_query_details(selected_query);
    if (issues.length > 0) {
        $('.line-chart').css({
            'visibility': 'visible'
        });
        $('.verify_ignore_chart').css({
            'visibility': 'visible'
        });
        $('.general-details').css({
            'visibility': 'visible'
        });
        $('.general-details-body').css({
            'visibility': 'visible'
        });
        $('.chart-line').css({
            'visibility': 'visible'
        });
        $('.view-btn').css({
            'visibility': 'visible'
        });
        $('.sort-btn').css({
            'visibility': 'visible'
        });
        $('.button-row').css({
            'visibility': 'visible'  
        });
        $('#nomatching').remove();
        var list_view_front_index = 0;
        for (var element of issues) {
            $(".card-deck").append(build_issue(element));
            list_view_front_index += 1;
            if (list_view_front_index > 39) {
                break;
            }
        }
        localStorage.list_view_front_index = list_view_front_index;

        $(function () {
            $('.example-popover').popover({
                container: 'body'
            })
        });
        
        add_reopen();
        add_button_implementation();
        build_flywheel(data.scores);
        update_total_issues_chart(selected_query);
        update_general_issue_information(selected_query);
        update_bottom_event()
    } else {
        $('#nomatching').remove();
        $('#card-deck').append('<div id="nomatching">No matching queries</div>');
        $('.line-chart').css({
            'visibility': 'hidden'
        });
        $('.verify_ignore_chart').css({
            'visibility': 'hidden'
        });
        $('.general-details').css({
            'visibility': 'hidden'
        });
        $('.general-details-body').css({
            'visibility': 'hidden'
        });
        $('.chart-line').css({
            'visibility': 'hidden'
        });
        $('.view-btn').css({
            'visibility': 'hidden'
        });
        $('.sort-btn').css({
            'visibility': 'hidden'
        });
        $('.button-row').css({
            'visibility': 'visible' 
        });
    }
}

function update_bottom_event() {
    $(window).scroll(function () {
        if ($(window).scrollTop() + window.innerHeight > ($(document).height() - 800) && get_active_view() == "list") {
            var data = JSON.parse(localStorage.issues);
            for (var x = parseInt(localStorage.list_view_front_index); x < (parseInt(localStorage.list_view_front_index) + 40); x++) {
                if (x < parseInt(localStorage.issue_back_index)) {
                    var element = data.issues[x];
                    $(".card-deck").append(build_issue(element));
                }
            }
            localStorage.list_view_front_index = parseInt(localStorage.list_view_front_index) + 40;
            $(function () {
                $('.example-popover').popover({
                    container: 'body'
                })
            });

            add_reopen();
            add_button_implementation();
            build_flywheel(data.scores);
        }
    });
}


function build_carousel(selected_query) {
    if (!selected_query || selected_query == -1) {
        return;
    }
    $(".issue").remove();

    $('.issues_carousel').css({
        'display': 'block'
    });

    $('.carousel_arrow').css({
        'display': 'inherit'
    });
    $('.carousel_arrow').removeClass('hidden-arrow');
    //Delete from carousel
    if ($(".issues_carousel").hasClass('slick-initialized')) {
        $('.issues_carousel').slick('unslick');
    }
    var data = JSON.parse(localStorage.issues);
    build_query_details(selected_query);
    if (data.issues.length > 3) {
        $('.carousel_arrow').css({
            'visibility': 'visible'
        });
        $('.line-chart').css({
            'visibility': 'visible'
        });
        $('.verify_ignore_chart').css({
            'visibility': 'visible'
        });
        $('.general-details').css({
            'visibility': 'visible'
        });
        $('.general-details-body').css({
            'visibility': 'visible'
        });
        $('.chart-line').css({
            'visibility': 'visible'
        });
        $('.view-btn').css({
            'visibility': 'visible'
        });
        $('.sort-btn').css({
            'visibility': 'visible'
        });
        $('.button-row').css({
            'visibility': 'visible'  
        });
        $('#nomatching').remove();
        var front_index = 0;
        var issues_length = data.issues.length;
        //add first 3 issues
        while (front_index < 3 && front_index < data.issues.length) {
            element = data.issues[front_index];
            $(".issues_carousel").append(build_issue(element));
            front_index += 1;
        }

        localStorage.issue_front_index = front_index;
        localStorage.issue_back_index = issues_length;

        $(function () {
            $('.example-popover').popover({
                container: 'body'
            })
        });

        $('.issues_carousel').slick({
            prevArrow: $('.prev'),
            nextArrow: $('.next'),
            infinite: true,
            slidesToShow: 3,
            slidesToScroll: 3,
            responsive: [
                {
                    breakpoint: 1200,
                    settings: {
                        slidesToShow: 2,
                        slidesToScroll: 2,
                    }
                },
                {
                    breakpoint: 800,
                    settings: {
                        slidesToShow: 1,
                        slidesToScroll: 1,
                    }
                }
            ]
        });
        add_reopen();
        add_button_implementation();
        add_left_arrow_impl();
        add_right_arrow_impl();
        build_flywheel(data.scores);
        update_total_issues_chart(selected_query);
        update_general_issue_information(selected_query);
    } else if (data.issues.length > 0 && data.issues.length < 4) {
        $('.carousel_arrow').css({
            'visibility': 'hidden'
        });
        $('.line-chart').css({
            'visibility': 'visible'
        });
        $('.verify_ignore_chart').css({
            'visibility': 'visible'
        });
        $('.general-details').css({
            'visibility': 'visible'
        });
        $('.general-details-body').css({
            'visibility': 'visible'
        });
        $('.chart-line').css({
            'visibility': 'visible'
        });
        $('.view-btn').css({
            'visibility': 'visible'
        });
        $('.sort-btn').css({
            'visibility': 'visible'
        });
        $('.button-row').css({
            'visibility': 'visible'  
        });
        $('#nomatching').remove();
        var front_index = 0;
        var issues_length = data.issues.length;
        //add first 3 issues
        while (front_index < 3 && front_index < data.issues.length) {
            element = data.issues[front_index];
            $(".issues_carousel").append(build_issue(element));
            front_index += 1;
        }

        localStorage.issue_front_index = front_index;
        localStorage.issue_back_index = issues_length;

        $(function () {
            $('.example-popover').popover({
                container: 'body'
            })
        });

        $('.issues_carousel').slick({
            prevArrow: $('.prev'),
            nextArrow: $('.next'),
            infinite: true,
            slidesToShow: 3,
            slidesToScroll: 3,
            responsive: [
                {
                    infinite: true,
                    breakpoint: 1200,
                    settings: {
                        slidesToShow: 2,
                        slidesToScroll: 2,
                    }
                },
                {
                    infinite: true,
                    breakpoint: 800,
                    settings: {
                        slidesToShow: 1,
                        slidesToScroll: 1,
                    }
                }
            ]
        });
        add_reopen();
        add_button_implementation();
        add_left_arrow_impl();
        add_right_arrow_impl();
        build_flywheel(data.scores);
        update_total_issues_chart(selected_query);
        update_general_issue_information(selected_query);
    } else {
        $('#nomatching').remove();
        $('#issues_carousel').append('<div id="nomatching">No matching queries</div>');
        update_total_issues_chart(selected_query);
        $('.carousel_arrow').css({
            'visibility': 'hidden'
        });
        $('.line-chart').css({
            'visibility': 'hidden'
        });
        $('.verify_ignore_chart').css({
            'visibility': 'hidden'
        });
        $('.general-details').css({
            'visibility': 'hidden'
        });
        $('.general-details-body').css({
            'visibility': 'hidden'
        });
        $('.chart-line').css({
            'visibility': 'hidden'
        });
        $('.view-btn').css({
            'visibility': 'hidden'
        });
        $('.sort-btn').css({
            'visibility': 'hidden'
        });
        $('.button-row').css({
            'visibility': 'visible'  
        });
    }
}

function update_general_issue_information(selected_query) {
    var general_issue_info_url = "./general_issue_info?query_id=" + selected_query
    $.ajax({
        url: general_issue_info_url,
        dataType: 'json',
        success: function (data) {
            if (data.avg_open_score && data.avg_open_score != "None") {
                $('#avg_open_score').text(' ' + parseFloat(data.avg_open_score).toFixed(2));
            } else {
                $('#avg_open_score').text(' N/A');
            }
            if (data.avg_verified_score && data.avg_verified_score != "None") {
                $('#avg_verified_score').text(' ' + parseFloat(data.avg_verified_score).toFixed(2));
            } else {
                $('#avg_verified_score').text(' N/A');
            }
            if (data.avg_ignored_score && data.avg_ignored_score != "None") {
                $('#avg_ignored_score').text(' ' + parseFloat(data.avg_ignored_score).toFixed(2));
            } else {
                $('#avg_ignored_score').text(' N/A');
            }
        }
    });
}

function add_right_arrow_impl() {
    $('.next').on('click', function () {
        var json_issues_response = JSON.parse(localStorage.issues);
        var json_issues = json_issues_response.issues;
        var scores = json_issues_response.scores;
        if (parseInt(localStorage.issue_back_index) > 3) {
            $('#issues_carousel').slick('slickRemove', null, null, true);
            var front_index = parseInt(localStorage.issue_front_index);
            for (var x = front_index; x < front_index + 3; x++) {
                var json_issue = json_issues[lp_val(x)];
                var element = build_issue(json_issue);
                localStorage.issue_front_index = lp_val(x+1);
                //slickAdd removes the two outter most divs for some reason
                $('#issues_carousel').slick('slickAdd', '<div><div>' + element + '</div></div>');
            }
            $(function () {
                $('.example-popover').popover({
                    container: 'body'
                })
            });
            add_reopen();
            add_button_implementation();
            build_flywheel(scores);
        }
    });

    $(document).keydown(function (event) {
        if (event.which == 39) {
            $('.next').trigger('click');
        }
    });
}


function add_left_arrow_impl() {
    $('.prev').on('click', function () {
        var json_issues_response = JSON.parse(localStorage.issues);
        var json_issues = json_issues_response.issues;
        var scores = json_issues_response.scores;
        if (parseInt(localStorage.issue_back_index) > 3) {
            $('#issues_carousel').slick('removeSlide', null, null, true);
            var front_index = parseInt(localStorage.issue_front_index);
            for(var x=front_index-6; x<front_index-3;x++){
                var json_issue = json_issues[lp_val(x)];
                var element = build_issue(json_issue);
                localStorage.issue_front_index = lp_val(x+1);
                //slickAdd removes the two outer most div for some reason
                $('#issues_carousel').slick('slickAdd', '<div><div>' + element + '</div></div>');
            }
            $(function () {
                $('.example-popover').popover({
                    container: 'body'
                })
            });
            
        }
        add_reopen();
            add_button_implementation();
            build_flywheel(scores);
    });

    $(document).keydown(function (event) {
        if (event.which == 37) {
            $('.prev').trigger('click');
        }
    });
}

function lp_val(val) {
    var length = parseInt(localStorage.issue_back_index);
    if (val < 0) {
        return (length - ((val * -1) % length));
    }
    else {
        return (val % length)
    }
}


function build_queries() {
    queries_url = "./queries?filters="
    if (localStorage.open_filter_enabled == undefined || localStorage.open_filter_enabled == 1) {
        queries_url += 'open,';
    }
    if (localStorage.ignored_filter_enabled == 1) {
        queries_url += 'ignored,';
    }
    if (localStorage.verified_filter_enabled == 1) {
        queries_url += 'verified,';
    }
    $.ajax({
        url: queries_url,
        dataType: "json",
        success: function (data) {
            var theDatabases = data.databases;
            for (var theDatabase of theDatabases) {
                $("#queries_list").append('<div id="' + theDatabase + '" class="database ' + theDatabase + '"> '+ theDatabase + ' </div> <u1 id="' + theDatabase);
            }
            var selected_query_id = parseInt(localStorage.selected_query);
            localStorage.queries = JSON.stringify(data);
            $.each(data.queries, function (_, element) {
                if (selected_query_id && element.id == selected_query_id) {
                    $('.database.'+element.database).append('</u1> <div id="' + element.id + '" class="query_selector selected_query"> ' + element.queryName + ' (' + element.issue_count + ') </div>');
                } else {
                    $('.database.'+element.database).append('</u1> <div id="' + element.id + '" class="query_selector"> ' + element.queryName + ' (' + element.issue_count + ') </div>');
                }
            });
            $(".query_selector").click(function () {
                $('.example-popover').popover('hide');
                $('.selected_query').removeClass('selected_query');
                $('#show-details-btn').removeClass('hidden');
                var selected_query = $(this).attr('id');
                $(this).addClass('selected_query');
                localStorage.selected_query = selected_query;
                update_issues_view(selected_query);
                build_carousel();
            });
            $(".query_selector").each(function () {
                $(this).prepend('<i class="the-car fa fa-car" aria-hidden="true"></i>');
            });
        }
    });
}

$(document).ready(function () {
    build_queries();
});


function build_score_div(element) {
    var score = element.overall_score;
    var color = perc2color((-1 * score) + 70);
    var response = '<div class="row score hexagon justify-content-center" style="border-top-color: ' + color + ';border-bottom-color:' + color + ';background-color:' + color + ';">';
    response += score.toFixed(0);
    response += '</div>'
    return response;
}

function build_issue_body(element) {
    dateTest = moment(element.date_opened).toDate().toString().slice(0, 24);
    formattedDate = moment(element.date_opened).add(5, 'hours').format('LLL')
    var response = '<div class="col">'
    if (element.queryValue.length < 50) {
        response += '<div class="row issue_header">' + element.queryValue + '</div>';
    } else {
        response += '<div class="row issue_header example-popover" data-container="body" data-toggle="popover" data-placement="left" data-html="true" data-content="' + element.queryValue + '">' + element.queryValue.slice(0, 50) + '...' + '</div>';
    }
    response += '<div class="row issue_score justify-content-center">' + build_score_div(element) + '</div>';
    if (element.context.length < 50) {
        response += '<div class="row context"><span><b>Context:&nbsp;</b>' + element.context + '</span></div>';
    } else {
        response += '<div class="row context example-popover" data-container="body" data-toggle="popover" data-placement="left" data-html="true" data-content="' + element.context + '"><span><b>Context:&nbsp;</b>' + element.context.slice(0, 50) + '</span>' + '...</div>';
    }
    if (element.suggestion.length < 50) {
        response += '<div class="row suggestion"><span><b>Suggestion:&nbsp;</b>' + element.suggestion + '</span></div>';
    } else {
        response += '<div class="row context example-popover" data-container="body" data-toggle="popover" data-placement="left" data-html="true" data-content="' + element.suggestion + '"><span><b>Suggestion:&nbsp;</b>' + element.suggestion.slice(0, 50) + '...</span></div>';
    }
    response += '<div class="row reported"><span><b>Reported:&nbsp;</b>' + formattedDate + '</span></div>';
    response += '<canvas id="flywheel_' + element.id + '" class="row flywheel"></canvas>';
    response += '<div class="row ignore-verify-buttons">' +
        '<div class="col">' +
        '<div class="row">'
    if (element.status != 'Ignored') {
        response += '<div id="ignore_' + element.id + '" class="btn status_btn ignore">Ignore</div>'
    }
    else {
        response += '<div id="ignore_' + element.id + '" class="btn status_btn ignore status_btn_active">Ignored</div>'
    }
    response += '</div>' +
        '</div>' +
        '<div class="col">' +
        '<div class="row">'
    if (element.status != 'Verified') {
        response += '<div id="verify_' + element.id + '" class="btn status_btn verify">Verify</div>'
    }
    else {
        response += '<div id="verify_' + element.id + '" class="btn status_btn verify status_btn_active">Verified</div>'
    }
    response += '</div>' +
        '</div>' +
        '</div>';
    response += '</div>';
    return response;
}

function build_issue(element) {
    var view = get_active_view();
    var response = '';
    if (view == 'list') {
        response = '<div class="card issue list_card">';
    } else {
        response = '<div class="card issue carousel_card">'
    }
    response += '<div class"card-body">' + build_issue_body(element) + '</div>';
    response += '</div>';
    return response;

}

function refresh_query_numbers() {
    $(".query_selector").remove();
    build_queries();
}

function build_flywheel(scores) {
    var stattechniques = JSON.parse(localStorage.queries).stattechniques
    var options = {
        legend: {
            position: 'left',
            labels: {
                boxWidth: 10,
                fontSize: 12,
                fontFamily: 'Roboto,-apple-system,BlinkMacSystemFont,"Segoe UI","Helvetica Neue",Arial,sans-serif,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol"',
            },
            usePointStyle: true
        },
        responsive: true,
        mainstainAspectRation: false,
        layout: {
            height: 500,
            width: 500
        }
    };

    $('.flywheel').each(function () {
        if (!$(this).hasClass('chartjs-render-monitor')) {
            var scores_data = [], labels_set = [];
            var query_weights = JSON.parse(localStorage.query_weights);
            var flywheel_id = $(this).attr('id').split('_')[1];
            for (var score of scores) {
                if (flywheel_id == score.issue_id) {
                    var stattechnique = stattechniques.filter(function (element) {
                        return score.statTechnique_id == element.id;
                    });
                    var query_weight = query_weights.filter(function (element) {
                        return element.statTechnique_id = element.id
                    })[0];
                    scores_data.push(((100 * score.score) * query_weight.weight).toFixed(2));
                    labels_set.push(stattechnique[0].statTechnique)
                }
            }
            var data = {
                datasets: [{
                    data: scores_data,
                    backgroundColor: [
                        '#F59CA9',
                        '#8E8DBE',
                        '#DD614A',
                        '#4FBBEE',
                        'rgba(54, 162, 235, 0.2)',
                        'rgba(255, 206, 86, 0.2)',
                    ],
                }],
                labels: labels_set
            };

            var ctx = document.getElementById($(this).attr('id')).getContext('2d');
            var myDoughnutChart = new Chart(ctx, {
                type: 'doughnut',
                data: data,
                options: options
            });
            myDoughnutChart.render();
        }
    });
}

$(document).ready(function () {
    $('#horkos-title').on('click', function () {
        update_issues_view(-1);
        $('.details').addClass('hidden');
        $('.example-popover').popover('hide');
        $('.show-details-btn').addClass('disabled-show-details-btn');
        $('#show-details-btn').addClass('hidden');
        $('.line-chart').css({
            'visibility': 'visible'
        });
        $('.verify_ignore_chart').css({
            'visibility': 'visible'
        });
        $('.general-details').css({
            'visibility': 'visible'
        });
        $('.general-details-body').css({
            'visibility': 'visible'
        });
        $('.chart-line').css({
            'visibility': 'visible'
        });
        $('.view-btn').css({
            'visibility': 'hidden'
        });
        $('.sort-btn').css({
            'visibility': 'hidden'
        });
        $('.button-row').css({
            'visibility': 'hidden'  
        });
    });
});

$(document).ready(function () {
    update_issues_view(-1);
    localStorage.selected_query = -1
    $('.details').addClass('hidden');
    $('#show-details-btn').addClass('hidden');
    $('.line-chart').css({
        'visibility': 'visible'
    });
    $('.verify_ignore_chart').css({
        'visibility': 'visible'
    });
    $('.general-details').css({
        'visibility': 'visible'
    });
    $('.general-details-body').css({
        'visibility': 'visible'
    });
    $('.chart-line').css({
        'visibility': 'visible'
    });
    $('.view-btn').css({
        'visibility': 'hidden'
    });
    $('.sort-btn').css({
        'visibility': 'hidden'
    });
    $('.button-row').css({
        'visibility': 'hidden'  
    });
});

$(document).ready(function () {
    if (localStorage.open_filter_enabled == 0) {
        if (!$('#open-filter-btn').hasClass('disabled-filter-btn')) {
            $('#open-filter-btn').addClass('disabled-filter-btn');
        }
    }
    if (localStorage.ignored_filter_enabled == 0 || localStorage.ignored_filter_enabled == undefined) {
        if (!$('#ignored-filter-btn').hasClass('disabled-filter-btn')) {
            $('#ignored-filter-btn').addClass('disabled-filter-btn');
        }
    }

    if (localStorage.verified_filter_enabled == 0 || localStorage.verified_filter_enabled == undefined) {
        if (!$('#verified-filter-btn').hasClass('disabled-filter-btn')) {
            $('#verified-filter-btn').addClass('disabled-filter-btn');
        }
    }

    $('#open-filter-btn').on('click', function () {
        open_filter_enabled = localStorage.open_filter_enabled === undefined ? 1 : localStorage.open_filter_enabled;
        if (open_filter_enabled == 1) {
            localStorage.open_filter_enabled = 0;
            $(this).addClass('disabled-filter-btn')
        } else {
            localStorage.open_filter_enabled = 1;
            if ($(this).hasClass('disabled-filter-btn')) {
                $(this).removeClass('disabled-filter-btn');
            }
        }
        refresh_query_numbers();
        update_issues_view(localStorage.selected_query);
    });

    $('#ignored-filter-btn').on('click', function () {
        ignored_filter_enabled = localStorage.ignored_filter_enabled === undefined ? 0 : localStorage.ignored_filter_enabled;
        if (ignored_filter_enabled == 1) {
            localStorage.ignored_filter_enabled = 0;
            $(this).addClass('disabled-filter-btn')
        } else {
            localStorage.ignored_filter_enabled = 1;
            if ($(this).hasClass('disabled-filter-btn')) {
                $(this).removeClass('disabled-filter-btn');
            }
        }
        refresh_query_numbers();
        update_issues_view(localStorage.selected_query);
    });

    $('#verified-filter-btn').on('click', function () {
        verified_filter_enabled = localStorage.verified_filter_enabled === undefined ? 0 : localStorage.verified_filter_enabled;
        if (verified_filter_enabled == 1) {
            localStorage.verified_filter_enabled = 0;
            $(this).addClass('disabled-filter-btn')
        } else {
            localStorage.verified_filter_enabled = 1;
            if ($(this).hasClass('disabled-filter-btn')) {
                $(this).removeClass('disabled-filter-btn');
            }
        }
        refresh_query_numbers();
        update_issues_view(localStorage.selected_query);
    });
});

$(document).ready(function () {
    if (localStorage.sortby != undefined) {
        $('.sort-btn').text('Sort by: ' + localStorage.sortby);
    } else {
        $('.sort-btn').text('Sort by: Score');
    }
    $('.sort-btn-item').on('click', function () {
        var sort_value = $(this).text();
        localStorage.sortby = sort_value.trim();
        $('.sort-btn').text('Sort by: ' + sort_value);
        update_issues_view(localStorage.selected_query);
    });
});

function perc2color(perc) {
    var r, g, b = 0;
    if (perc < 50) {
        r = 255;
        g = Math.round(5.1 * perc);
    }
    else {
        g = 255;
        r = Math.round(510 - 5.10 * perc);
    }
    var h = r * 0x10000 + g * 0x100 + b * 0x1;
    return '#' + ('000000' + h.toString(16)).slice(-6);
}

$(document).ready(function () {
    $('#searchTerm').on('keyup', function () {
        var search_term = $(this).val().toLowerCase();
        $('.database').each(function () {
            var query_text = $(this).text().toLowerCase();
            if (query_text.includes(search_term)) {
                $(this).css({
                    'display': 'inherit'
                });
            } else {
                $(this).css({
                    'display': 'None'
                });
            }
        });
    });
});


function renderChart(data_set){
    if (window.myLine != null) {
        window.myLine.destroy();
    }
    var ctx = document.getElementById("line-chart").getContext('2d');
    var config = {
        type: 'line',
        data: {
            datasets: [{
                label: 'Issue Count',
                borderColor: "rgba(142, 141, 190, 1)",
                backgroundColor: "rgba(142, 141, 190, 0.5)",
                fill: true,
                data: data_set,
                pointRadius: 0,
            }]
        },
        options: {
            responsive: true,
            legend: {
                display: false
            },
            title: {
                display: false
            },
            scales: {
                xAxes: [{
                    type: 'time',
                    display: true,
                    scaleLabel: {
                        display: true,
                        labelString: 'Date',
                        fontFamily: 'Roboto,-apple-system,BlinkMacSystemFont,"Segoe UI","Helvetica Neue",Arial,sans-serif,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol"',
                        fontColor: "#595959",
                        fontSize: 14,
                        fontStyle: 700
                    },
                    ticks: {
                            autoSkip: false,
                            maxRotation: 0,
                            minRotation: 0,
                            fontFamily: 'Roboto,-apple-system,BlinkMacSystemFont,"Segoe UI","Helvetica Neue",Arial,sans-serif,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol"',
                            fontColor: "#595959"
                    },
                    gridLines: {
                        display: false
                    }
                }],
                yAxes: [{
                    display: true,
                    stacked: true,
                    ticks: {
                        fontFamily: 'Roboto,-apple-system,BlinkMacSystemFont,"Segoe UI","Helvetica Neue",Arial,sans-serif,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol"',
                        fontColor: "#595959",
                    },
                    scaleLabel: {
                        display: true,
                        labelString: '# of Issues',
                        fontFamily: 'Roboto,-apple-system,BlinkMacSystemFont,"Segoe UI","Helvetica Neue",Arial,sans-serif,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol"',
                        fontColor: "#595959",
                        fontSize: 14,
                        fontStyle: 700
                    },
                    gridLines: {
                        display: false
                    }
                }]
            }
        }
    };
    window.myLine = new Chart(ctx, config);
};



function update_total_issues_chart(selected_query) {
    var issues_url = '';
    if (selected_query == undefined || selected_query == -1) {
        issues_url = "./issues_chart_api?filters=Open,Ignored,Verified"
    } else {
        issues_url = "./issues_chart_api?query_id=" + selected_query + "&filters=Open,Ignored,Verified"
    }
    $.ajax({
        url: issues_url,
        dataType: "json",
        success: function (issues_data) {
            var data = [];
            var issues = issues_data.issues;
            var issue_count = 0;
            var prev_date = ""
            var formattedDate = ""
            for (var issue of issues) {
                formattedDate = moment(issue.date_opened).add(5, 'hours')
                issue_count += 1;
                if (prev_date != formattedDate || issues[issue.length - 1] == issue) {
                    data.push({
                        x: formattedDate,
                        y: issue_count
                    });
                }
                prev_date = formattedDate;
            }
            if (issue_count != 0) {
                renderChart(data);
            }
            else {
                window.myLine.destroy();
            }
            update_open_verified_chart(issues_data.issues);
        }
    });
};

$(document).ready(function () {
    $('#details').addClass('hidden');
    $('.show-details-btn').on('click', function () {
        if ($(this).hasClass('disabled-show-details-btn')) {
            $(this).removeClass('disabled-show-details-btn');
            //Hide details
            $('#details').removeClass('hidden');
        } else {
            $(this).addClass('disabled-show-details-btn');
            //Show details
            $('#details').addClass('hidden');
        }
    });
});

function show_screen_issues() {
    $('.issues_carousel').css({
        'visibility': 'visible'
    });
    $('.issues_carousel').removeClass('hidden');
    $('.card-deck').css({
        'visibility': 'visible'
    });
    $('.card-deck').removeClass('hidden');
    $('.carousel_arrow').css({
        'visibility': 'visible'
    });
    $('.carousel_arrow').removeClass('hidden');
    $('.domain_chart_wrapper').addClass('hidden');
}

function clear_screen_issues() {
    $('.selected_query').removeClass('selected_query');
    $('.issues_carousel').css({
        'visibility': 'hidden'
    });
    $('.issues_carousel').addClass('hidden');
    $('.card-deck').css({
        'visibility': 'hidden'
    });
    $('.card-deck').addClass('hidden');
    $('.carousel_arrow').css({
        'visibility': 'hidden'
    });
    $('.carousel_arrow').addClass('hidden');
    $('.domain_chart_wrapper').removeClass('hidden');
}

function add_domain_chart() {
    if (window.domain_chart != null) {
        window.domain_chart.destroy();
    }
    var element = document.getElementById('domain_chart');
    if (element == null) {
        $('.carousel-holder-row').append('<div class="card domain_chart_wrapper"><div class="card-header domain-chart-header"><b>Issues By Domain</b></div><div class="card-body domain-chart-body"><canvas id="domain_chart"></canvas></div></div>');
    }
    var api_url = './domain_spread_api?filters=Open,Verified,Ignored';
    $.ajax({
        dataType: 'json',
        url: api_url,
        success: function (data_set) {
            var chart_labels = [];
            var chart_data = [];
            Object.entries(data_set).forEach(([key, value]) => {
                chart_labels.push(key);
                chart_data.push(value);
            });
            var data = {
                "labels": chart_labels,
                "datasets": [{
                    "label": "issues",
                    "data": chart_data,
                    "fill": false,
                    "backgroundColor": ["rgba(245, 156, 169, 0.5)", "rgba(221, 97, 74, 0.5)", "rgba(255, 159, 64, 0.5)", "rgba(127, 190, 171, 0.5)", "rgba(79, 187, 238, 0.5)", "rgba(142, 141, 190, 0.5)", "rgba(201, 203, 207, 0.5)"],
                    "borderColor": ["rgb(245, 156, 169)", "rgb(221, 97, 74)", "rgb(255, 159, 64)", "rgb(127, 190, 171)", "rgb(79, 187, 238)", "rgb(142, 141, 190)", "rgb(201, 203, 207)"],
                    "borderWidth": 3
                }]
            };
            var options = {
                aspectRatio: 3,
                "legend": {
                    "display": false
                },
                "scales": {
                    "xAxes": [{
                        "gridLines": {
                            "display": false
                        },
                    }],
                    "yAxes": [{
                        display: false,
                        "gridLines": {
                            "display": false
                        },
                        "ticks": {
                            "beginAtZero": true,
                            "display": false
                        }
                    }]
                },
                "title": {
                    "display": false
                },
            };
            var ctx = document.getElementById("domain_chart").getContext('2d');
            window.domain_chart = new Chart(ctx, {
                type: 'bar',
                data: data,
                options: options
            });
        }
    });
}

function update_issues_view(selected_query) {
    if (!selected_query || selected_query == -1) {
        update_total_issues_chart(selected_query);
        update_general_issue_information(selected_query);
        clear_screen_issues();
        add_domain_chart();
        return;
    }
    show_screen_issues();
    issues_url = "./issues_api?query_id=" + selected_query + "&filters="
    if (localStorage.open_filter_enabled == undefined || localStorage.open_filter_enabled == 1) {
        issues_url += 'open,';
    }
    if (localStorage.ignored_filter_enabled == 1) {
        issues_url += 'ignored,';
    }
    if (localStorage.verified_filter_enabled == 1) {
        issues_url += 'verified,';
    }
    if (localStorage.sortby == 'Date') {
        issues_url += '&sortby=Date';
    } else {
        issues_url += '&sortby=Score';
    }
    $.ajax({
        url: issues_url,
        dataType: "json",
        success: function (data) {
            localStorage.issues = JSON.stringify(data);
            if (get_active_view() == 'carousel') {
                build_carousel(selected_query)
            }
            if (get_active_view() == 'list') {
                build_issue_list(selected_query)
            }
        }
    });
}

function get_active_view() {
    if (!$('.list-view-btn').hasClass('disabled-view-btn')) {
        return 'list'
    } else {
        return 'carousel'
    }
}

$(document).ready(function () {
    $('.view-btn').on('click', function () {
        $('.example-popover').popover('hide');
        $('.view-btn').each(function () {
            if ($(this).hasClass('disabled-view-btn')) {
                $(this).removeClass('disabled-view-btn');
                update_issues_view(localStorage.selected_query);
            } else {
                $(this).addClass('disabled-view-btn');
            }
        });
    });
});


function update_open_verified_chart(issues) {
    if (window.open_verify_chart != null) {
        window.open_verify_chart.destroy();
    }
    var chart_data = [];
    var opened = 0;
    var verified = 0;
    for (var issue of issues) {
        if (issue.status == "Open") {
            opened += 1;
        }
        if (issue.status == "Verified") {
            verified += 1;
        }
    }
    chart_data.push(opened);
    chart_data.push(verified);

    var data = {
        "labels": ["Open", "Verified"],
        "datasets": [{
            "label": "issues",
            "data": chart_data,
            "fill": false,
            "backgroundColor": ["rgba(245, 156, 169, 0.5)", "rgba(255, 159, 64, 0.5)"],
            "borderColor": ["rgb(245, 156, 169)", "rgb(255, 159, 64)"],
            "borderWidth": 2
        }]
    };
    var options = {
        aspectRatio: 1,
        "legend": {
            "display": true,
            labels: {
                fontFamily: 'Roboto,-apple-system,BlinkMacSystemFont,"Segoe UI","Helvetica Neue",Arial,sans-serif,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol"',
                fontColor: "#595959",
                fontSize: 14,
                fontStyle: 700
            }
        },
        "scales": {
            "xAxes": [{
                display: false
            }],
            "yAxes": [{
                display: false
            }]
        },
        "title": {
            "display": false
        },
    };
    var ctx = document.getElementById("verify_ignore_chart").getContext('2d');
    window.open_verify_chart = new Chart(ctx, {
        type: 'pie',
        data: data,
        options: options
    });
}
