%% _____________MAIN CODE_____________%%
clc
close all

users_list = dir('dataset');
file_list=[];
for nUser=3:size(users_list)
    files=dir(['dataset/', users_list(nUser).name]);
    for iFile=1:size(files)
        if files(iFile).isdir==0
            file_list=[file_list;files(iFile)];    
        end
    end
end
% Function - Features Computation 
[WFeat, Name, Weka, AllFeatures] = HAR_Features (file_list); 
    
arffwrite_HAR('HAR_52participants', AllFeatures, Name)

%%FILE .ARFF for Weka
function arffwrite_HAR(filename, data, attribute_names)
    arff_file = fopen([filename, '.arff'], 'w');

    % Write relation
    fprintf(arff_file, '@relation %s\n\n', filename);

    % Write attributes
    for i = 1:length(attribute_names)
        fprintf(arff_file, '@attribute %s numeric\n', attribute_names{i});
    end

    % Write data
    fprintf(arff_file, '\n@data\n');
    for i = 1:size(data, 1)
        fprintf(arff_file, '%s\n', num2str(data(i, :), '%f,'));
    end

    fclose(arff_file);
end


