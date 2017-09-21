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
        <div className="wrap">
           <div className="search">
              <input type="text" value={this.state.searchString} onChange={this.handleChange} className="searchTerm"
              placeholder="Search for a city or building"/>
           </div>
        </div>
        <ul>
          { buildings.map(function(building){ 
            var building_string = building.city + ' ' + building.name;
            if (building.height){
              building_string += ' (' + building.height +'m)';
            }
            building_string += ' '+building.status;
            return <li><a href={building.link} target="_blank">{building_string}</a></li> }) }
        </ul>
      </div>
    )
  }

});

ReactDOM.render(
  <DynamicSearch items={ buildings } />,
  document.getElementById('list')
);
