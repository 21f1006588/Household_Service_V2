<template>
  <div class="signuppage">
    <!-- Header Bar -->
    <header class="header-bar">
      <div class="header-left">
        <img src="@/assets/logo.jpg" class="logo" alt="Logo" />
        <h1 class="site-title">Household Services Application</h1>
      </div>
      <nav class="header-nav">
        <ul>
          <li><router-link to="/">Home</router-link></li>
          <li><router-link to="/admin_login">Admin Login</router-link></li>
          <li><router-link to="/user_login">User Login</router-link></li>
          <li class="active"><router-link to="/user_signup">User Signup</router-link></li>
        </ul>
      </nav>
    </header>

    <!-- Hero Section -->
    <section class="hero">
      <div class="hero-overlay"></div>
      <div class="hero-content">
        <!-- Signup Form Container -->
        <div class="signup-form">
          <h2>Sign-Up</h2>
          <!-- Error Handling -->
          <p class="alert" v-if="error_1">{{ error_1 }}</p>

          <!-- Full Name -->
          <div class="txt_field">
            <input type="text" v-model="fullname" placeholder="Full Name" minlength="3" maxlength="200" required />
          </div>

          <!-- Email-ID -->
          <div class="txt_field">
            <input type="email" v-model="email" placeholder="Email-ID" maxlength="40" required />
          </div>

          <!-- Username -->
          <div class="txt_field">
            <input type="text" v-model="username" placeholder="Username" minlength="3" required />
          </div>

          <!-- Password -->
          <div class="txt_field">
            <input type="password" v-model="password" placeholder="Password" minlength="8" required />
          </div>

          <!-- User Type Selection -->
          <div class="txt_field">
            <select v-model="user_type" required>
              <option disabled value="">Select User Type</option>
              <option value="customer">Customer</option>
              <option value="service_professional">Service Professional</option>
            </select>
          </div>

          <!-- Additional Fields for Service Professional -->
          <div v-if="user_type === 'service_professional'">
            <!-- Phone Number -->
            <div class="txt_field">
              <input type="text" v-model="phone_number" placeholder="Phone Number" required />
            </div>
            <!-- Service Type -->
            <div class="txt_field">
              <input type="text" v-model="service_type" placeholder="Service Type" required />
            </div>
            <!-- Experience (years) -->
            <div class="txt_field">
              <input type="number" v-model="experience" placeholder="Experience (years)" required />
            </div>
            <!-- Location -->
            <div class="txt_field">
              <input type="text" v-model="location" placeholder="Location" required />
            </div>
            <!-- Pincode -->
            <div class="txt_field">
              <input type="text" v-model="pincode" placeholder="Pincode" required />
            </div>
          </div>

          <!-- Submit Button -->
          <div class="form-actions">
            <button @click="register" class="btn">Sign-Up</button>
          </div>

          <p class="signup_link">
            Already have an account? <router-link :to="{ name: 'user_login' }">Login</router-link>
          </p>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
export default {
  name: "SignupPage",
  data() {
    return {
      fullname: null,
      email: null,
      username: null,
      password: null,
      user_type: "",
      phone_number: null,
      service_type: null,
      experience: null,
      location: null,
      pincode: null,
      error_1: ""
    };
  },
  created() {
    sessionStorage.clear();
    localStorage.clear();
  },
  updated() {
    sessionStorage.clear();
    localStorage.clear();
  },
  methods: {
    async register() {
      if (this.emailValidation(this.email) && this.passValidation(this.password)) {
        try {
          const response = await fetch("http://127.0.0.1:5000/api/user", {
            method: "POST",
            headers: {
              "Access-Control-Allow-Origin": "*",
              "Content-Type": "application/json"
            },
            body: JSON.stringify({
              fullname: this.fullname,
              email: this.email,
              username: this.username,
              password: this.password,
              user_type: this.user_type,
              phone_number: this.user_type === "service_professional" ? this.phone_number : null,
              service_type: this.user_type === "service_professional" ? this.service_type : null,
              experience: this.user_type === "service_professional" ? this.experience : null,
              location: this.user_type === "service_professional" ? this.location : null,
              pincode: this.user_type === "service_professional" ? this.pincode : null
            })
          });
          if (response.ok) {
            console.log("Registered");
            alert("Registered Successfully");
            this.$router.push("/login");
          } else if (response.status === 400) {
            this.error_1 = "The email you entered already belongs to an account. Try another email.";
            alert(this.error_1);
          } else if (response.status === 500) {
            this.error_1 = "The username you entered already belongs to an account. Try another username.";
            alert(this.error_1);
          }
        } catch (error) {
          console.log("Registration Failed:", error);
          alert(error);
        }
      } else if (!this.emailValidation(this.email)) {
        this.error_1 = "Please enter a valid email";
        alert(this.error_1);
      } else if (!this.passValidation(this.password)) {
        this.error_1 = "Password requires at least 8 characters.";
        alert(this.error_1);
      }
    },
    emailValidation(email) {
      var result =
        /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
      return result.test(email);
    },
    passValidation(pass) {
      var result = /.{8,}/;
      return result.test(pass);
    }
  }
};
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
.header-nav ul li a:hover,
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
  color: yellow;
}

/* ===== SIGN-UP FORM ===== */
.signup-form {
  background: white;
  padding: 2rem;
  border-radius: 10px;
  border: 3px solid black;
  box-shadow: 0 4px 10px grey;
  width: 400px;
  min-height: 300px;
}
.signup-form h2 {
  margin-bottom: 1rem;
  color: #333;
}
.txt_field {
  margin: 1rem 0;
}
.txt_field input,
.txt_field select {
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
  color: black;
}
.signup_link a {
  color: blue;
  text-decoration: none;
}
.signup_link a:hover {
  text-decoration: none;
  color: blue;
}
</style>
