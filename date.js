const currentDate = new Date()
const formattedDate = currentDate.toISOString().slice(0,19).replace('T',' ');
console.log(formattedDate,currentDate)    
