var right = -2;
var months = [
  "Jan",
  "Feb",
  "März",
  "Apr",
  "Mai",
  "Juni",
  "Juli",
  "Aug",
  "Sep",
  "Okt",
  "Nov",
  "Dez"
];

$(function() {

  loader("loader");

  $(document).on("swipeup", "#hoge", function(event) {
    if (event.type !== "release") {
      console.log("up");
      $("body")
        .removeClass()
        .addClass("animated  faster slideInUp");

      rendererArticle();
    }
  });

  $(document).on("swipedown", "#hoge", function(event) {
    if (event.type !== "release") {
      console.log("down");
    }
  });

  $(document).on("swipeleft", "#hoge", function(event) {
    if (event.type !== "release") {
      setContent("left");
    }
  });

  $(document).on("swiperight", "#hoge", function(event) {
    if (event.type !== "release") {
      setContent("right");
    }
  });
});

function loader(page) {
  $.get(page + ".html", function(data) {
    $("body").html(data);
  });
}

function closeArticle() {
  $("body")
    .removeClass()
    .addClass("animated faster slideInDown");
  loader("card-screen");
  setTimeout(function() {
    setContent("");
    console.log("called");
  }, 50);
}

function changeColor(element) {
  $(".button--outline").css({ "background-color": "", color: "" });

  $("#" + element.id + ".button--outline").css({
    "background-color": "#0076ff",
    color: "#fff"
  });
  console.log(element.id);
}

function rendererArticle() {
  loader("article-screen");
}

function setContent(position) {


  if (position == "left") {
    $("body")
      .removeClass()
      .addClass("animated  faster slideInRight");
    console.log("right");

    if (right === -1) right = 10;
    --right;
  }
 else if (position == "right") {
    $("body")
      .removeClass()
      .addClass("animated  faster slideInLeft");
    console.log("right");

    if (right === 9) right = -1;
    ++right
  }else right++

  setTimeout(function(){  
 
  $(".example-1 .wrapper").css(
    "background",
    "url(" + main_data.result[right].image_url + ") center / cover no-repeat"
  );

  $(".title").text(main_data.result[right].title);

  $(".text").text(main_data.result[right].subtitle);

  $(".author").text(
    "Lesezeit: " + main_data.result[right].timetoread + " Minute(n)"
  );

  var d = new Date(main_data.result[right].release_date);

  $(".day").text(d.getDate());

  $(".month").text(months[d.getMonth()]);

  $(".year").text(d.getFullYear());

}, 300);
}
