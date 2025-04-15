const formatFloat = (number) => {
  let formattedNumber = new Intl.NumberFormat('en-EN', {
    useGrouping: false,
    //minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(number);
  return formattedNumber;
};

export default formatFloat;
