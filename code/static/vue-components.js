const navbar = {
  template: //html
  `
  <section class="row text-center">
    <div class="f1">
      <button class="tab-btn" @click=" goTo('app-create-user')">Create User</button>
    </div>
    <div class="f1">
      <button class="tab-btn" @click="goTo('app-login')">Login</button>
    </div>
    <div class="f1">
      <button class="tab-btn" @click="goTo('app-user-list')">View Users</button>
    </div>
  </section>
  `,
  methods: {
    goTo(component) {
      EventBus.$emit('go-to', component);
    }
  }
}

const login = {
  template: //html
  `
  <div>
    <h3>Login</h3>
  </div>
  `,
}

const createUser = {
  template: //html
  `
  <div>
    <h3>Create User</h3>
    <section class="row">
      <div class="f1">
        <label for="username">
          Username:
          <input type="text" id="username" name="username" v-model="username" />
        </label>
      </div>
      <div class="f1">
        <label for="password">
          Password:
          <input type="password" id="password" name="password" v-model="password" />
        </label>
      </div>
    </section>
  </div>
  `,
  data: function() {
    return {
      username: '',
      password: '',
    };
  },
  methods: {

  }
}

const userList = {
  template: //html
  `
  <div>
    <h3>User List</h3>
    <button @click="doThis">Clicky clicky</button>
  </div>
  `,
  methods: {
    doThis: function() {      
      EventBus.$emit('something', { msg: 'Hello' })
    }
  }
}