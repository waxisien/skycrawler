var DynamicSearch = React.createClass({

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
      <div>
        <input id="search-btn" type="text" value={this.state.searchString} onChange={this.handleChange} placeholder="Search!" />
        <ul>
          { buildings.map(function(building){ 
            return <li><a href={building.link} target="_blank">{building.city + ' ' + building.name}</a></li> }) }
        </ul>
      </div>
    )
  }

});

ReactDOM.render(
  <DynamicSearch items={ buildings } />,
  document.getElementById('list')
);
