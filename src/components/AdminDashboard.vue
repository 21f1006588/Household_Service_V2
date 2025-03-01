<template>
  <div class="admin-dashboard">
    <!-- Dashboard Top Header -->
    <div class="dashboard-header">
      <h2>Welcome, {{ admin.username }}!</h2>
      <button @click="logout" class="logout-btn">Logout</button>
    </div>

    <!-- Search Form -->
    <div class="search-container">
      <form @submit.prevent="search">
        <input 
          type="text" 
          v-model="search_query" 
          placeholder="Search by name" 
          required
        />
        <button type="submit" class="search-btn">Search</button>
      </form>
    </div>

    <!-- Search Results Section (if any) -->
    <section v-if="search_query">
      <h3>Search Results for "{{ search_query }}"</h3>
      
      <!-- Matching Customers -->
      <h4>Matching Customers</h4>
      <div v-if="customers && customers.length">
        <table>
          <thead>
            <tr>
              <th>Name</th>
              <th>Username</th>
              <th>Email</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="customer in customers" :key="customer.id">
              <td>{{ customer.name }}</td>
              <td>{{ customer.username }}</td>
              <td>{{ customer.email }}</td>
              <td>
                <!-- Block/Unblock actions can go here -->
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-else>
        <p>No matching customers found.</p>
      </div>

      <!-- Matching Service Professionals -->
      <h4>Matching Service Professionals</h4>
      <div v-if="professionals && professionals.length">
        <table>
          <thead>
            <tr>
              <th>Name</th>
              <th>Service Type</th>
              <th>Location</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="professional in professionals" :key="professional.id">
              <td>{{ professional.name }}</td>
              <td>{{ professional.service_type }}</td>
              <td>{{ professional.location }}</td>
              <td>
                <!-- Approve/Reject actions can go here -->
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-else>
        <p>No matching service professionals found.</p>
      </div>

      <!-- Matching Services -->
      <h4>Matching Services</h4>
      <div v-if="services && services.length">
        <table>
          <thead>
            <tr>
              <th>Name</th>
              <th>Description</th>
              <th>Price</th>
              <th>Time Required</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="service in services" :key="service.id">
              <td>{{ service.name }}</td>
              <td>{{ service.description }}</td>
              <td>${{ service.price }}</td>
              <td>{{ service.time_required }} mins</td>
              <td>
                <!-- Edit/Delete actions -->
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-else>
        <p>No matching services found.</p>
      </div>
    </section>

    <!-- Pending Service Professional Registrations -->
    <section class="pending-section">
      <h3>Pending Service Professional Registrations</h3>
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Service Type</th>
            <th>Location</th>
            <th>Experience</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="professional in pending_professionals" :key="professional.id">
            <td>{{ professional.name }}</td>
            <td>{{ professional.service_type }}</td>
            <td>{{ professional.location }}</td>
            <td>{{ professional.experience }} years</td>
            <td>
              <button @click="approveProfessional(professional.id)" class="approve-btn">Approve</button>
              <button @click="rejectProfessional(professional.id)" class="reject-btn">Reject</button>
            </td>
          </tr>
        </tbody>
      </table>
    </section>

    <!-- Services Management -->
    <section class="services-section">
      <div class="services-header">
        <h3>Manage Services</h3>
        <button @click="createService" class="add-service-btn">
          <i class="fas fa-plus"></i> Add New Service
        </button>
      </div>
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Description</th>
            <th>Price</th>
            <th>Time Required</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="service in servicesList" :key="service.id">
            <td>{{ service.name }}</td>
            <td>{{ service.description }}</td>
            <td>${{ service.price }}</td>
            <td>{{ service.time_required }} mins</td>
            <td>
              <button @click="editService(service.id)" class="edit-btn">Edit</button>
              <button @click="deleteService(service.id)" class="delete-btn">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
    </section>

    <!-- All Users -->
    <section class="users-section">
      <h3>All Users</h3>
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Username</th>
            <th>Email</th>
            <th>User Type</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in allUsers" :key="user.id">
            <td>{{ user.name }}</td>
            <td>{{ user.username }}</td>
            <td>{{ user.email }}</td>
            <td>{{ user.user_type }}</td>
            <td>
              <button v-if="user.is_blocked" @click="unblockUser(user.id, user.user_type)" class="unblock-btn">Unblock</button>
              <button v-else @click="blockUser(user.id, user.user_type)" class="block-btn">Block</button>
            </td>
          </tr>
        </tbody>
      </table>
    </section>
  </div>
</template>

<script>
export default {
  name: "AdminDashboard",
  data() {
    return {
      admin: {},
      search_query: "",
      customers: [],
      professionals: [],
      services: [],
      pending_professionals: [],
      servicesList: [],
      allUsers: []
    };
  },
  created() {
    this.fetchDashboardData();
  },
  methods: {
    logout() {
      // Implement logout logic here
      sessionStorage.clear();
      this.$router.push("/");
    },
    fetchDashboardData() {
      // Replace this with an actual API call to fetch data.
      // For demonstration, we use dummy data.
      this.admin = { username: "AdminUser" };
      this.customers = []; // Populate with customer objects
      this.professionals = []; // Populate with service professional objects
      this.services = []; // Populate with service objects (from search)
      this.pending_professionals = []; // Populate with pending professionals
      this.servicesList = []; // Populate with all services
      this.allUsers = []; // Populate with all users
    },
    search() {
      // Implement search logic (update customers, professionals, and services arrays based on search_query)
      alert("Searching for: " + this.search_query);
    },
    approveProfessional(id) {
      // Implement API call to approve professional
      alert("Approved professional with ID: " + id);
    },
    rejectProfessional(id) {
      // Implement API call to reject professional
      alert("Rejected professional with ID: " + id);
    },
    createService() {
      this.$router.push("/create_service");
    },
    editService(id) {
      this.$router.push({ name: "edit_service", params: { service_id: id } });
    },
    deleteService(id) {
      if (confirm("Are you sure you want to delete this service?")) {
        alert("Deleted service with ID: " + id);
      }
    },
    blockUser(id) {
    alert("Blocked user with ID: " + id);
    },
    unblockUser(id) {
    alert("Unblocked user with ID: " + id);
    }
  }
};
</script>

<style scoped>
.admin-dashboard {
  padding: 20px;
  font-family: Arial, Helvetica, sans-serif;
}

/* Dashboard Header */
.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
}
.dashboard-header h2 {
  padding: 50px;
  margin-bottom: auto;
  color: rgb(13, 51, 223);
}
.logout-btn {
  margin-top: 35px;
  padding: 12px;
  background-color: #e74c3c;
  color: white;
  border: none;
  border-radius: 5px;
  font-size: 1.1em;
  cursor: pointer;
}
.logout-btn:hover {
  background-color: #c0392b;
}

/* Search Container */
.search-container {
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 20px 0;
}
.search-container form {
  display: flex;
  align-items: center;
  width: 100%;
  max-width: 1000px;
  gap: 0;
}
.search-container input[type="text"] {
  flex-grow: 1;
  padding: 5px;
  font-size: 1em;
  border-radius: 5px;
  border: 2px solid #181616;
  border-right: none;
}
.search-container .search-btn {
  padding: 5px 5px;
  font-size: 1em;
  border: none;
  border-radius: 5px;
  background-color: #45a049;
  color: white;
  cursor: pointer;
  white-space: nowrap;
}
.search-container .search-btn:hover {
  background-color: #3d8b3d;
}

/* Tables */
table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 20px;
}
table, th, td {
  border: 1px solid #ddd;
}
th, td {
  padding: 10px;
  text-align: left;
}
th {
  background-color: #f2f2f2;
}
section h3, section h4 {
  margin-top: 20px;
  text-decoration: underline;
}

/* Buttons for Tables */
.approve-btn, .reject-btn, .unblock-btn, .block-btn, .edit-btn, .delete-btn, .add-service-btn {
  padding: 8px 12px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 0.9em;
}
.approve-btn {
  background-color: #4CAF50;
  color: white;
}
.reject-btn {
  background-color: #e74c3c;
  color: white;
}
.unblock-btn, .block-btn {
  background-color: #3498db;
  color: white;
}
.edit-btn {
  background-color: #f39c12;
  color: white;
}
.delete-btn {
  background-color: #e74c3c;
  color: white;
}
.add-service-btn {
  background-color: #45a049;
  color: white;
  padding: 10px;
  font-size: 1em;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .dashboard-header {
    flex-direction: column;
    align-items: flex-start;
  }
  .dashboard-header h2 {
    padding: 20px 0;
  }
  table, th, td {
    font-size: 0.8em;
  }
}
</style>
