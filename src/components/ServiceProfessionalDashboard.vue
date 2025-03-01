<template>
  <div class="dashboard">
    <!-- Dashboard Header -->
    <div class="dashboard-header">
      <h2>Welcome, {{ professional.name }}!</h2>
      <button @click="logout" class="logout-btn">Logout</button>
    </div>

    <!-- Professional Info -->
    <div class="professional-info">
      <p>Service Type: {{ professional.service_type }}</p>
      <p>Location: {{ professional.location }}</p>
      <p>Pincode: {{ professional.pincode }}</p>
      <p>Experience: {{ professional.experience }} years</p>
    </div>

    <!-- Assigned Service Requests Section -->
    <section class="assigned-requests">
      <h3>Assigned Service Requests</h3>
      <table v-if="assigned_requests.length">
        <thead>
          <tr>
            <th>Service Name</th>
            <th>Customer</th>
            <th>Phone</th>
            <th>Request Date</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="request in assigned_requests" :key="request.id">
            <td>{{ request.service.name }}</td>
            <td>{{ request.customer.name }}</td>
            <td>{{ request.customer.phone_number }}</td>
            <td>{{ formatDate(request.date_of_request) }}</td>
            <td>{{ request.service_status }}</td>
            <td>
              <button
                v-if="request.service_status === 'accepted'"
                @click="markComplete(request.id)"
                class="complete-btn"
              >
                Mark as Complete
              </button>
            </td>
          </tr>
        </tbody>
      </table>
      <p v-else>No assigned service requests.</p>
    </section>

    <!-- Pending Service Requests Section -->
    <section class="pending-requests">
      <h3>Pending Service Requests</h3>
      <table v-if="pending_requests.length">
        <thead>
          <tr>
            <th>Service Name</th>
            <th>Customer</th>
            <th>Phone</th>
            <th>Request Date</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="request in pending_requests" :key="request.id">
            <td>{{ request.service.name }}</td>
            <td>{{ request.customer.name }}</td>
            <td>{{ request.customer.phone_number }}</td>
            <td>{{ formatDate(request.date_of_request) }}</td>
            <td>
              <button @click="acceptRequest(request.id)" class="accept-btn">
                Accept
              </button>
              <button @click="rejectRequest(request.id)" class="reject-btn">
                Reject
              </button>
            </td>
          </tr>
        </tbody>
      </table>
      <p v-else>
        No pending service requests available for your service type.
      </p>
    </section>
  </div>
</template>

<script>
export default {
  name: "ServiceProfessionalDashboard",
  data() {
    return {
      // Dummy data; replace these with API results as needed.
      professional: {
        name: "Service Pro",
        service_type: "Electrical",
        location: "New York",
        pincode: "10001",
        experience: 5
      },
      assigned_requests: [
        {
          id: 1,
          service: { name: "Electrical Repair" },
          customer: { name: "Alice", phone_number: "123-456-7890" },
          date_of_request: "2023-04-01T00:00:00Z",
          service_status: "accepted"
        }
      ],
      pending_requests: [
        {
          id: 2,
          service: { name: "Electrical Installation" },
          customer: { name: "Bob", phone_number: "987-654-3210" },
          date_of_request: "2023-04-05T00:00:00Z"
        }
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
      // fetch(`http://api.example.com/dashboard?email=${sessionStorage.getItem("email")}`)
      //   .then(resp => resp.json())
      //   .then(data => {
      //      this.professional = data.professional;
      //      this.assigned_requests = data.assigned_requests;
      //      this.pending_requests = data.pending_requests;
      //   })
      //   .catch(error => console.error(error));
    },
    logout() {
      sessionStorage.clear();
      this.$router.push("/login");
    },
    markComplete(requestId) {
      // Implement API call to mark request as complete.
      alert("Marking request " + requestId + " as complete");
    },
    acceptRequest(requestId) {
      // Implement API call to accept the request.
      alert("Accepted request " + requestId);
    },
    rejectRequest(requestId) {
      // Implement API call to reject the request.
      alert("Rejected request " + requestId);
    },
    formatDate(dateStr) {
      if (!dateStr) return "";
      return new Date(dateStr).toLocaleDateString();
    }
  }
};
</script>

<style scoped>
/* Dashboard Container */
.dashboard {
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
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 5px;
  font-size: 1.1em;
  cursor: pointer;
}
.logout-btn:hover {
  background-color: #45a049;
}

/* Professional Info */
.professional-info p {
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
th,
td {
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

/* Buttons for Tables */
.accept-btn,
.reject-btn,
.complete-btn {
  padding: 8px 12px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 0.9em;
}
.accept-btn {
  background-color: #4CAF50;
  color: white;
}
.reject-btn {
  background-color: #e74c3c;
  color: white;
}
.complete-btn {
  background-color: #3498db;
  color: white;
}

/* Responsive Adjustments */
@media (max-width: 768px) {
  .dashboard-header {
    flex-direction: column;
    align-items: flex-start;
  }
  .dashboard-header h2 {
    padding: 20px 0;
  }
  table,
  th,
  td {
    font-size: 0.9em;
  }
}
</style>
