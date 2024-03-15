document.addEventListener('DOMContentLoaded', () => {
    (document.querySelectorAll('.notification .delete') || []).forEach(($delete) => {
        const $notification = $delete.parentNode;
        $delete.addEventListener('click', () => {
        $notification.parentNode.removeChild($notification);
        });
    });
});

document.body.style.cursor = "default";

const apikey='BP8GPRYV53UQ56SHJR5EFCJ77'
const myCity='Guildford'
const webapi=`https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/weatherdata/forecast?aggregateHours=24&contentType=json&unitGroup=metric&locationMode=single&key=${apikey}&locations=${myCity}`;
fetch(webapi)
    .then((response) => {
        return response.json();
    })
    .then((data) => {
        const cityInfo = document.getElementById('cityinfo');
        let todayCondition = `  Now: ${data.location.currentConditions.temp}&#8451 ${data.location.values[0].conditions}`;
        let tmrCondition = `  Tomorrow: ${data.location.values[1].temp}&#8451 ${data.location.values[1].conditions}`;
        cityInfo.innerHTML = myCity.concat(todayCondition,'; ',tmrCondition);
    })
    .catch(function(error) {
        cityInfo.innerHTML = error;
    });

function onPageRefresh() {
    document.body.style.cursor = "progress";
    const cursorStyle = document.createElement('style');
    cursorStyle.innerHTML = '*{cursor: progress;}';
    cursorStyle.id = 'cursor-style';
    document.head.appendChild(cursorStyle);
}