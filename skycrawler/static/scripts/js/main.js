(function e(t,n,r){function s(o,u){if(!n[o]){if(!t[o]){var a=typeof require=="function"&&require;if(!u&&a)return a(o,!0);if(i)return i(o,!0);var f=new Error("Cannot find module '"+o+"'");throw f.code="MODULE_NOT_FOUND",f}var l=n[o]={exports:{}};t[o][0].call(l.exports,function(e){var n=t[o][1][e];return s(n?n:e)},l,l.exports,e,t,n,r)}return n[o].exports}var i=typeof require=="function"&&require;for(var o=0;o<r.length;o++)s(r[o]);return s})({1:[function(require,module,exports){
var DynamicSearch = React.createClass({displayName: "DynamicSearch",

  // sets initial state
  getInitialState: function(){
    return { searchString: '' };
  },

  // sets state, triggers render method
  handleChange: function(event){
    // grab value form input box
    this.setState({searchString:event.target.value});
    console.log("scope updated!");
  },

  render: function() {

    var buildings = this.props.items;
    var searchString = this.state.searchString.trim().toLowerCase();

    // filter buildings list by value from input box
    if(searchString.length > 0){
      buildings = buildings.filter(function(building){
        return building.city.toLowerCase().match( searchString ) || building.name.toLowerCase().match( searchString );
      });
    }

    return (
      React.createElement("div", null, 
        React.createElement("div", {className: "wrap"}, 
           React.createElement("div", {className: "search"}, 
              React.createElement("input", {type: "text", value: this.state.searchString, onChange: this.handleChange, className: "searchTerm", 
              placeholder: "Search for a city or building"})
           )
        ), 
        React.createElement("ul", null, 
           buildings.map(function(building){ 
            var building_string = building.city + ' ' + building.name;
            if (building.height){
              building_string += ' (' + building.height +'m)';
            }
            building_string += ' '+building.status;
            return React.createElement("li", null, React.createElement("a", {href: building.link, target: "_blank"}, building_string)) }) 
        )
      )
    )
  }

});

ReactDOM.render(
  React.createElement(DynamicSearch, {items:  buildings }),
  document.getElementById('list')
);

},{}]},{},[1]);
