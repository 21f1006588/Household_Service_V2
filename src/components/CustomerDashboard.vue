<template>
  <div class="customer-dashboard">
    <!-- Header with Welcome Message and Logout -->
    <div class="dashboard-header">
      <h2>Welcome, {{ customer.name }}!</h2>
      <button @click="logout" class="logout-btn">Logout</button>
    </div>

    <!-- Customer Info -->
    <div class="customer-info">
      <p>Email: {{ customer.email }}</p>
      <p>Phone: {{ customer.phone_number }}</p>
    </div>

    <!-- Available Services Section -->
    <section class="available-services">
      <h3>Available Services</h3>
      <table>
        <thead>
          <tr>
            <th>Service Name</th>
            <th>Description</th>
            <th>Price</th>
            <th>Time Required</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="service in availableServices" :key="service.id">
            <td>{{ service.name }}</td>
            <td>{{ service.description }}</td>
            <td>${{ formatPrice(service.price) }}</td>
            <td>{{ service.time_required }} minutes</td>
          </tr>
        </tbody>
      </table>
    </section>

    <!-- Service Requests Section -->
    <section class="service-requests">
      <div class="requests-header">
        <h3>Your Service Requests</h3>
        <button @click="createServiceRequest" class="create-request-btn">
          <i class="fas fa-plus"></i> Create Service Request
        </button>
      </div>
      <table>
        <thead>
          <tr>
            <th>Service Name</th>
            <th>Description</th>
            <th>Requested On</th>
            <th>Completed On</th>
            <th>Remarks</th>
            <th>Actions</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="request in customer.service_requests" :key="request.id">
            <td><strong>{{ request.service.name }}</strong></td>
            <td>{{ request.service.description }}</td>
            <td>{{ formatDate(request.date_of_request) }}</td>
            <td>
              <span v-if="request.service_status === 'closed'">
                {{ formatDate(request.date_of_completion) }}
              </span>
              <span v-else>N/A</span>
            </td>
            <td>{{ request.remarks ? request.remarks : "None" }}</td>
            <td>
              <button @click="editServiceRequest(request.id)" class="edit-btn">Edit</button>
              <button
                v-if="request.service_status !== 'closed'"
                @click="closeServiceRequest(request.id)"
                class="close-btn"
              >
                Close
              </button>
            </td>
            <td>
              <span v-if="request.service_status === 'requested'">Pending</span>
              <span v-else-if="request.service_status === 'accepted'">Accepted</span>
              <span v-else-if="request.service_status === 'rejected'">Rejected</span>
              <span v-else-if="request.service_status === 'closed'">Completed</span>
            </td>
          </tr>
        </tbody>
      </table>
    </section>
  </div>
</template>

<script>
export default {
  name: "CustomerDashboard",
  data() {
    return {
      // Dummy data; replace with API call results
      customer: {
        name: "John Doe",
        email: "john@example.com",
        phone_number: "123-456-7890",
        service_requests: [
          {
            id: 1,
            service: { name: "Plumbing", description: "Fix leaking faucet" },
            date_of_request: "2023-01-01T00:00:00Z",
            date_of_completion: "2023-01-03T00:00:00Z",
            remarks: "Fixed quickly",
            service_status: "closed"
          },
          {
            id: 2,
            service: { name: "Cleaning", description: "House cleaning" },
            date_of_request: "2023-02-01T00:00:00Z",
            date_of_completion: null,
            remarks: "",
            service_status: "requested"
          }
        ]
      },
      availableServices: [
        { id: 1, name: "Plumbing", description: "Fix leaking faucet", price: 50.0, time_required: 30 },
        { id: 2, name: "Cleaning", description: "House cleaning service", price: 80.0, time_required: 90 }
      ]
    };
  },
  created() {
    this.fetchDashboardData();
  },
  methods: {
    fetchDashboardData() {
      // Replace this stub with your API call to fetch dashboard data.
      // For example:
      // fetch(`http://127.0.0.1:5000/api/customer_dashboard?email=${sessionStorage.getItem("email")}`)
      //   .then(resp => resp.json())
      //   .then(data => {
      //      this.customer = data.customer;
      //      this.availableServices = data.available_services;
      //   })
      //   .catch(error => console.error(error));
    },
    logout() {
      // Implement logout logic (clear session and redirect)
      sessionStorage.clear();
      this.$router.push("/login");
    },
    createServiceRequest() {
      this.$router.push("/create_service_request");
    },
    editServiceRequest(requestId) {
      this.$router.push({ name: "edit_service_request", params: { requestId } });
    },
    closeServiceRequest(requestId) {
      if (confirm("Are you sure you want to close this service request?")) {
        // Call your API to close the request, then refresh data.
        alert("Request " + requestId + " closed");
        this.fetchDashboardData();
      }
    },
    formatDate(dateStr) {
      if (!dateStr) return "";
      const date = new Date(dateStr);
      return date.toLocaleDateString();
    },
    formatPrice(price) {
      return price.toFixed(2);
    }
  }
};
</script>

<style scoped>
.customer-dashboard {
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
  padding: 60px;
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

/* Customer Info */
.customer-info p {
  font-size: 1.1em;
  margin: 10px 20px;
}

/* Section Titles */
section h3 {
  margin: 20px 0;
  text-decoration: underline;
}

/* Tables */
table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 20px;
}
th, td {
  border: 1px solid #ddd;
  padding: 8px;
}
th {
  background-color: #f4f4f4;
  text-align: left;
}
tr:nth-child(even) {
  background-color: #f9f9f9;
}
tr:hover {
  background-color: #f1f1f1;
}

/* Requests Header */
.requests-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 0;
}
.create-request-btn {
  background-color: #45a049;
  color: white;
  padding: 10px;
  font-size: 1em;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
.create-request-btn:hover {
  background-color: #3d8b3d;
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
    font-size: 0.9em;
  }
}
</style>
