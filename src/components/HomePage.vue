<template>
  <div class="homie">
    <!-- Top Header Bar -->
    <header class="header-bar">
      <div class="header-left">
        <img src="@/assets/logo.jpg" class="logo" alt="Logo" />
        <h1 class="site-title">Household Services Application</h1>
      </div>
      <nav class="header-nav">
        <ul>
          <li class="active"><a href="/">Home</a></li>
          <li><a href="/admin_login">Admin Login</a></li>
          <li><a href="/user_login">User Login</a></li>
          <li><a href="/user_signup">User Signup</a></li>
          <li><a href="/admin_dashboard">Admin Dashboard</a></li>
          <li><a href="/customer_dashboard">Customer Dashboard</a></li>
          <li><a href="/service_professional_dashboard">SP Dashboard</a></li>
        </ul>
      </nav>
    </header>

    <!-- Hero Section -->
    <section class="hero">
      <div class="hero-overlay"></div>
      <div class="hero-content">
        <h2 class="hero-title">"Strive not to be a success, but rather to be of value."</h2>
      </div>
    </section>
  </div>
</template>

<script>
export default {
  name: 'HomePage'
}
</script>

<style scoped>
/* Reset / Base */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: Arial, Helvetica, sans-serif;
}

/* Make sure parent containers fill viewport if needed */
html, body {
  width: 100%;
  height: 100%;
}

/* ===== HEADER BAR ===== */
.header-bar {
  height: 70px;          /* or however tall you want your header */
  display: flex;
  align-items: center;
  justify-content: space-between;
  background-color: #fff; /* White background */
  padding: 0 1rem;
  /* ...other styles... */
}

/* Left side: logo + site title */
.header-left {
  display: flex;
  align-items: center;
}
.logo {
  width: 60px;
  height: auto;
  margin-right: 1rem;
}
.site-title {
  font-size: 1.2rem;
  font-weight: bold;
}

/* Right side: nav */
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
  /* If you want to center content: */
  display: flex;
  align-items: center;
  justify-content: center;
  align-items: flex-start;
}

/* Semi-transparent overlay */
.hero-overlay {
  position: absolute;
  inset: 0; /* top:0, right:0, bottom:0, left:0 */
  background: rgba(0, 0, 0, 0.2); /* Adjust transparency as needed */
  z-index: 1;
}

/* Actual hero content */
.hero-content {
  position: relative;
  z-index: 2;
  text-align: center;
  max-width: 600px;
  color: yellow; /* If overlay is dark, switch to white (#fff) */
  margin-top: 2rem;
}

.hero-title {  
  font-size: 1.8rem;
  margin-bottom: 0.5rem;
  text-shadow: 1px 1px 2px #999;
}

.hero-buttons .btn {
  font-weight: bold;
  border: 3px solid black;
  padding: 0.5rem 1.5rem;
  margin: 0 0.5rem;
  color: black;
  text-decoration: none;
  background-color: aqua;
  transition: 0.3s ease;
}

.hero-buttons .btn:hover {
  background-color: black;
  color: wheat;
}
</style>
