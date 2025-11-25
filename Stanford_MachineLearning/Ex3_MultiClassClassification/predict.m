function p = predict(Theta1, Theta2, X)
%PREDICT Predict the label of an input given a trained neural network
%   p = PREDICT(Theta1, Theta2, X) outputs the predicted label of X given the
%   trained weights of a neural network (Theta1, Theta2)

% Useful values
m = size(X, 1);
num_labels = size(Theta2, 1);

% You need to return the following variables correctly 
p = zeros(size(X, 1), 1);

% ====================== YOUR CODE HERE ======================
% Instructions: Complete the following code to make predictions using
%               your learned neural network. You should set p to a 
%               vector containing labels between 1 to num_labels.
%
% Hint: The max function might come in useful. In particular, the max
%       function can also return the index of the max element, for more
%       information see 'help max'. If your examples are in rows, then, you
%       can use max(A, [], 2) to obtain the max for each row.
%

%%Below is an implementation of the formula in Figure 2 on p. 11 of ex3.pdf:

% Add ones to the X data matrix
a1 = [ones(m, 1) X]; %(5000x401)

% z2 is Theta(1)*a(1)--i.e., X*theta' as in previous exercises,
%% where here X is a1
z2 = a1*Theta1'; %(5000x401) x (401x25) => (5000x25)


m_z2 = size(z2, 1); % size(z2) = 5000x25 as above; m_z2 = 5000
a2 = [ones(m_z2, 1) sigmoid(z2)]; %(5000x26)

a3 = sigmoid(a2*Theta2'); %(5000x26) x (26x10) => (5000x10)

[v p] = max(a3,[],2);

% =========================================================================

end
