// 3. Create src/views/Students.vue
<template>
  <v-container>
    <h2>Students</h2>
    <v-table>
      <thead>
        <tr>
          <th>Student Number</th>
          <th>Name</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="s in students" :key="s.student_number">
          <td>{{ s.student_number }}</td>
          <td>{{ s.first_name }} {{ s.last_name }}</td>
        </tr>
      </tbody>
    </v-table>
  </v-container>
</template>

<script>
import api from '../api';

export default {
  data() {
    return { students: [] };
  },
  mounted() {
    api.get('/students')
      .then(res => this.students = res.data)
      .catch(err => console.error(err));
  }
};
</script>
