var main_data;

$.get("https://unsere-server.herokuapp.com/getFeed", function(data) {
  console.log(data);
  main_data = data;
  loader("card-screen");

  setContent();
});
