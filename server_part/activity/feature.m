%% Filtering 
% BandPass Filter Butterworth - 4th order
fs = 32;           % Sampling frequency
f_cut = 15;        % Cut-off frequency

% Read the accelerometer data from the CSV file
data = csvread('output.csv');

% Apply Butterworth filter
[b, a] = butter(4, f_cut/(fs/2), 'low');
filtered_data = filter(b, a, data);

% Write the filtered data to a new CSV file
csvwrite('filtered_data.csv', filtered_data);

% Plot original and filtered data
t = (0:size(data, 1)-1) / fs;
figure;
subplot(2, 1, 1);
plot(t, data);
title('Original Accelerometer Data');
xlabel('Time (s)');
ylabel('Acceleration');

subplot(2, 1, 2);
plot(t, filtered_data);
title('Filtered Accelerometer Data');
xlabel('Time (s)');
ylabel('Filtered Acceleration');
