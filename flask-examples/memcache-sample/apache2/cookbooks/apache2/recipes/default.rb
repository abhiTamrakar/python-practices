#
# Cookbook:: apache2 and Python
# Recipe:: default
#
# Copyright:: 2017, The Authors, All Rights Reserved.
package 'Install Apache' do
  case node[:platform]
  when 'redhat', 'centos'
    package_name 'httpd'
  when 'ubuntu', 'debian'
    package_name 'apache2'
  end
end

package %w(python python-pip memcached python-memcache libapache2-mod-wsgi) do
  action :install
end

execute 'install flask' do
  command 'pip install flask python-memcached'
end

service 'memcached' do
  supports :status => true, :restart => true, :reload => true
  action [ :enable, :start ]
end

service 'apache2' do
  supports :status => true, :restart => true, :reload => true
  action [ :enable, :restart ]
end

cookbook_file '/tmp/configure_apache.sh' do
  source 'configure_apache.sh'
  owner 'root'
  group 'root'
  mode '0755'
  action :create
end

cookbook_file '/tmp/layout.html' do
  source 'layout.html'
  owner 'root'
  group 'root'
  mode '0755'
  action :create
end

cookbook_file '/tmp/test.html' do
  source 'test.html'
  owner 'root'
  group 'root'
  mode '0755'
  action :create
end

cookbook_file '/tmp/localhost.crt' do
  source 'localhost.crt'
  owner 'root'
  group 'root'
  mode '0644'
  action :create
end

cookbook_file '/tmp/app.py' do
  source 'app.py'
  owner 'root'
  group 'root'
  mode '0755'
  action :create
end

cookbook_file '/tmp/app.wsgi' do
  source 'app.wsgi'
  owner 'root'
  group 'root'
  mode '0755'
  action :create
end

cookbook_file '/tmp/localhost.key' do
  source 'localhost.key'
  owner 'root'
  group 'root'
  mode '0644'
  action :create
end

template '/etc/apache2/sites-available/app.conf' do
  source 'localhost.conf.erb'
  owner 'root'
  group 'root'
  mode '0755'
end

template '/tmp/index.html' do
  source 'index.html.erb'
  owner 'root'
  group 'root'
  mode '0755'
end

bash 'configure apache' do
  user 'root'
  code '/tmp/configure_apache.sh'
end
