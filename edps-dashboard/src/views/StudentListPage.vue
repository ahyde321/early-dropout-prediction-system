<template>
    <v-container>
      <h2 class="mb-4">Student Directory</h2>
  
      <v-text-field
        v-model="search"
        label="Search"
        class="mb-4"
        prepend-inner-icon="mdi-magnify"
        clearable
      />
  
      <v-data-table
        :headers="headers"
        :items="filteredStudents"
        :search="search"
        :items-per-page="10"
        class="elevation-1"
      >
        <template v-slot:no-data>
          <v-alert type="info">No matching students found.</v-alert>
        </template>
  
        <template v-slot:item="props">
          <td>{{ props.item.student_number }}</td>
          <td>{{ props.item.first_name }}</td>
          <td>{{ props.item.last_name }}</td>
        </template>
      </v-data-table>
    </v-container>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name: 'StudentListView',
    data() {
      return {
        students: [],
        search: '',
        headers: [
          { text: 'Student Number', value: 'student_number' },
          { text: 'First Name', value: 'first_name' },
          { text: 'Last Name', value: 'last_name' },
        ],
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
            console.log(baseURL); // Check the data
            console.log(res.data); // Check the data
            this.students = res.data; // Store the student data
        })
        .catch((err) => {
          console.error('❌ Failed to fetch students:', err); // Log error if it fails
        });
    },
  };
  </script>
  
  <style scoped>
  h2 {
    font-weight: 600;
  }
  </style>
  