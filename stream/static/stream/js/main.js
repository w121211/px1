var Noodle = Noodle || {};

/* Init page */
$( function() {
    /* testing */
//    console.log(Noodle.LiveTag.json);
//    console.log(Noodle.LiveTag.render(Noodle.LiveTag.json));

    //Noodle.Channel.load();
    Noodle.Post.load();
    registEvents();
});

/* register elements with specific ajax actions */
var registEvents = function() {
    /* channel */
//    $(document).on("click", "a.channel-btn", Noodle.Channel.clickChannel);
    // $(document).on("click", "a.viewThread", Noodle.Channel.newChannel);
    //$(document).on("click", "a.viewThread", Noodle.Channel.tagChannel);
    // $(document).on("click", "a.channel-btn", Noodle.Channel.getChannels);

    /* stream */
//    $(document).on("click", "a.loadPosts", Noodle.Post.load);
    //$(document).on("click", , Noodle.Post.load);
//    $(document).on("click", "a.post_form_new", Noodle.Post.new);
    $(document).on("click", Noodle.Dom.Post.FORM_AUTOTAG_BTN, Noodle.Post.autotag);
//    $(document).on("click", "a.replyPost", Noodle.Post.reply);
//    $(document).on("keypress", "textarea.pushText", Noodle.Post.push);

    //$(document).on("click", "a.voteTag", noodle.ajax.voteTag);

    /* kaleido */
    /*
    $(document).on("click", "a.viewThread", noodle.ajax.loadThread); // not implemented
    */
};