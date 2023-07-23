$(document).ready(function() {
    $("#registrationForm").on('submit', function(e) {
        var url = $("#channelUrl").val();
        
        var regexPattern = /^(https:\/\/stand\.fm\/channels\/.+|https:\/\/www\.youtube\.com\/.+\/videos|https:\/\/open\.spotify\.com\/show\/.+|https:\/\/tver\.jp\/series\/.+|https:\/\/radiotalk\.jp\/program\/.+|https:\/\/radiko\.jp\/persons\/.+)$/;
        if (!url.match(regexPattern)) {
            alert("Please provide a valid URL. The URL must follow one of the following patterns:\nhttps://stand.fm/channels/{any_value}\nhttps://www.youtube.com/{any_value}/videos\nhttps://open.spotify.com/show/{any_value}\nhttps://tver.jp/series/{any_value}\nhttps://radiotalk.jp/program/{any_value}\nhttps://radiko.jp/persons/{any_value}");
            e.preventDefault();
        }
    });    
});
