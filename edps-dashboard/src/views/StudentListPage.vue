<template>
  <div class="p-6">
    <h2 class="text-2xl font-semibold mb-4">Student Directory</h2>

    <!-- Search Box -->
    <div class="mb-4">
      <input
        type="text"
        v-model="search"
        placeholder="Search students..."
        class="w-full p-2 border border-gray-300 rounded shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
      />
    </div>

    <!-- Student Table -->
    <div class="overflow-auto">
      <table class="min-w-full bg-white border border-gray-200 rounded shadow-sm">
        <thead>
          <tr class="bg-gray-100 text-left text-sm font-semibold text-gray-700">
            <th class="py-2 px-4 border-b">Student Number</th>
            <th class="py-2 px-4 border-b">First Name</th>
            <th class="py-2 px-4 border-b">Last Name</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="student in filteredStudents"
            :key="student.student_number"
            class="hover:bg-gray-50 text-sm"
          >
            <td class="py-2 px-4 border-b">{{ student.student_number }}</td>
            <td class="py-2 px-4 border-b">{{ student.first_name }}</td>
            <td class="py-2 px-4 border-b">{{ student.last_name }}</td>
          </tr>
          <tr v-if="filteredStudents.length === 0">
            <td colspan="3" class="py-4 px-4 text-center text-gray-500">
              No matching students found.
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'StudentListView',
  data() {
    return {
      students: [],
      search: '',
    };
  },
  computed: {
    filteredStudents() {
      const query = this.search.toLowerCase();
      return this.students.filter((student) =>
        Object.values(student).some((value) =>
          value.toString().toLowerCase().includes(query)
        )
      );
    },
  },
  mounted() {
    const baseURL = process.env.VUE_APP_API_BASE_URL || 'http://localhost:8000';

    axios
      .get(`${baseURL}/students/list`)
      .then((res) => {
        console.log('✅ Fetched students:', res.data);
        this.students = res.data;
      })
      .catch((err) => {
        console.error('❌ Failed to fetch students:', err);
      });
  },
};
</script>

<style scoped>
/* Optional scoped styles */
</style>
