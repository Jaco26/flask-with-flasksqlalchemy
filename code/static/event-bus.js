const EventBus = new Vue({
  
  methods: {
    handleSomething: function() {
      console.log('Hello from something!');
      
    }
  },
  mounted: function() {
    this.$on('something', this.handleSomething)
  },
})

function hi() {
  console.log('hi');
  
}

EventBus.$on('something', hi)