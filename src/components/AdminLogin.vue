<template>
  <div class="loginpage">
    <!-- Top Header Bar -->
    <header class="header-bar">
      <div class="header-left">
        <img src="@/assets/logo.jpg" class="logo" alt="Logo" />
        <h1 class="site-title">Household Services Application</h1>
      </div>
      <nav class="header-nav">
        <ul>
          <li><router-link to="/">Home</router-link></li>
          <li class="active"><router-link to="/admin_login">Admin Login</router-link></li>
          <li><router-link to="/user_login">User Login</router-link></li>
          <li><router-link to="/user_signup">User Signup</router-link></li>
        </ul>
      </nav>
    </header>

    <!-- Hero Section with Background Image -->
    <section class="hero">
      <div class="hero-overlay"></div>
      <div class="hero-content">
        <!-- Admin Login Form -->
        <div class="login-form">
          <h2>Admin Login</h2>
          <!-- Error Handling -->
          <p class="alert" v-if="error_1">{{ error_1 }}</p>
          <p class="alert" v-if="error_2">{{ error_2 }}</p>
          <div class="txt_field">
            <input type="email" v-model="email" placeholder="Email ID" required />
          </div>
          <div class="txt_field">
            <input type="password" v-model="password" placeholder="Password" required minlength="8" pattern=".{8,}" />
          </div>
          <div class="form-actions">
            <button @click="login" class="btn">Login</button>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
export default {
  name: 'AdminLoginPage',
  data() {
    return {
      email: null,
      password: null,
      error_1: "",
      error_2: "",
      auth: null,
      is_authenticated: false
    }
  },
  async created() {
    sessionStorage.clear();
    localStorage.clear();
  },
  async updated() {
    sessionStorage.clear();
    localStorage.clear();
  },
  methods: {
    async login() {
      try {
        fetch("http://127.0.0.1:5000/login?include_auth_token", {
          method: "POST",
          headers: {
            "Access-Control-Allow-Origin": "*",
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            email: this.email,
            password: this.password,
            is_authenticated: true
          })
        })
          .then((resp) => resp.json())
          .then(async (data) => {
            const { response } = data;
            console.log(data);
            if (response.errors) {
              if (response.errors[1]) {
                this.error_1 = response.errors[1];
                alert(this.error_1);
              }
              this.error_2 = response.errors[0];
              alert(this.error_2);
              console.log(this.error_1, this.error_2);
            } else {
              this.auth = response.user.authentication_token;
              sessionStorage.setItem("auth-token", this.auth);
              sessionStorage.setItem("email", this.email);
              this.$router.push("userfeed");
              console.log("its homepage");
            }
          })
          .catch((error) => {
            console.log("some error first time", error);
            alert(error);
          });
      } catch (error) {
        console.log("No way home: ", error);
        alert(error);
      }
    }
  }
}
</script>

<style scoped>
/* Reset & Base */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: Arial, Helvetica, sans-serif;
}
html, body {
  width: 100%;
  height: 100%;
}

/* ===== HEADER BAR ===== */
.header-bar {
  height: 70px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  background-color: #fff;
  padding: 0 1rem;
}
.header-left {
  display: flex;
  align-items: center;
}
.logo {
  width: 60px;
  margin-right: 1rem;
}
.site-title {
  font-size: 1.2rem;
  font-weight: bold;
}

/* Navigation */
.header-nav ul {
  list-style-type: none;
  display: flex;
}
.header-nav ul li {
  margin-left: 1rem;
}
.header-nav ul li a {
  font-weight: bold;
  text-decoration: none;
  color: black;
  padding: 0.5rem 1rem;
  border: 3px solid black;
  background-color: aqua;
  transition: 0.3s ease;
}
.header-nav ul li a:hover {
  background-color: black;
  color: wheat;
}
.header-nav ul li.active a {
  background-color: black;
  color: wheat;
}

/* ===== HERO SECTION ===== */
.hero {
  height: calc(100vh - 70px);
  background: url("@/assets/home.jpg") center center fixed no-repeat;
  background-size: cover;
  position: relative;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
}
.hero-overlay {
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.2);
  z-index: 1;
}
.hero-content {
  position: relative;
  z-index: 2;
  text-align: center;
  max-width: 600px;
  color: yellow; /* Adjust as needed */
}

/* ===== LOGIN FORM ===== */
.login-form {
  background: white;
  padding: 2rem;
  border-radius: 10px;
  border: 3px solid black;
  box-shadow: 0 4px 10px grey;
  width: 400px;      /* Increase the width */
  min-height: 200px; /* Increase the height, or use height if you prefer a fixed height */
}

.login-form h2 {
  margin-bottom: 1rem;
  color: #333;
}
.txt_field {
  margin: 1rem 0;
}
.txt_field input {
  width: 100%;
  padding: 0.5rem;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 5px;
}
.form-actions {
  margin: 1rem 0;
}
.btn {
  font-weight: bold;
  border: 3px solid black;
  padding: 0.5rem 1.5rem;
  background-color: aqua;
  color: black;
  cursor: pointer;
  transition: 0.3s ease;
  width: 100%;
}
.btn:hover {
  background-color: black;
  color: wheat;
}
.alert {
  color: red;
  margin-bottom: 1rem;
}

/* ===== SIGNUP LINK STYLING ===== */
.signup_link {
  margin-top: 1rem;
  font-size: 16px;
  color: black;  /* Text in black */
}
.signup_link a {
  color: blue;   /* Link text in blue */
  text-decoration: none;  /* Remove underline */
}
.signup_link a:hover {
  text-decoration: none;
  color: blue;
}
</style>
