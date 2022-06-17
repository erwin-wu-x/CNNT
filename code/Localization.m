% load PSF
PSF = load("PSF.mat");
PSF = PSF.PSF;

parfor i = 0 : 23999
localization(i,PSF);
end

function localization(i, PSF)
% load data
I = imread("data/"+num2str(i)+".png");
I = im2double(I);
I = rgb2gray(I);

% interpolate
interpolated = imresize(I, 10);

% 2-D normalized cross-correlation
cross_correlation = normxcorr2(PSF, interpolated);

% cut off the extra part result from the 2-D normalized cross-correlation
x = round((size(cross_correlation,1)-size(interpolated,1))/2);
y = round((size(cross_correlation,2)-size(interpolated,2))/2);
cross_correlation = cross_correlation(x+1:size(interpolated,1)+x,y+1:size(interpolated,2)+y);

% threshold
cross_correlation(cross_correlation<0.6)=0;

% get regional max
BW = imregionalmax(cross_correlation);

% open the output file
f = fopen("location/"+num2str(i)+".txt","w");

% write the result
for x = 1:size(BW,1)
    for y = 1:size(BW,2)
        if BW(x,y) == 1
            fprintf(f, "%f %f\n", x/10, y/10);
        end
    end
end
fclose(f);    
end
