#coding=utf

import struct

class Lex():
	
	def __init__(self,src_file,tar_file):
		self.file_head = '\x6D\x73\x63\x68\x78\x75\x64\x70\x01\x00\x00\x00\x40\x00\x00\x00'
		self.data_offset = '\x00\x00\x00\x00'
		self.file_length = '\x00\x00\x00\x00'
		self.word_count = 0 #'\x00\x00\x00\x00\x00\x00\x00\x00'
		self.file_date = '\x11\x11\x11\x11'
		self.null_data = '''\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'''
		self.word_offset = '' #'\x00\x00\x00\x00'
		self.word_start = '\x08\x00\x08\x00'
		self.word_length = '\x00\x00'
		self.word_local = '\x01\x06'
		self.word = ''
		self.word_delims = '\x00\x00'
		
		self.src_file = src_file
		self.tar_file = tar_file
		self.out2tar_file()
		
	def out2tar_file(self):
		file_data = self.init()
		# print str(file_data)
		f=open(self.tar_file,'wb')
		f.write(file_data)
		f.close()
		print 'Success!'
		
	def init(self):
		words = self.split_src_file()
		len_words = len(words)
		for line in words:
			try:
				words = line.split(',')
				if len(words)!=3:
					print line
					continue
				ci = words[0].decode('utf8').encode('unicode_escape').replace('\u','')
				bin_ci = ''
				i1 = ci[2::4]
				i2 = ci[3::4]
				i3 = ci[0::4]
				i4 = ci[1::4]
				for i,j,m,n in zip(i1,i2,i3,i4):
					bin_ci += (i+j+m+n).decode('hex')
				# print bin_ci.encode('hex')
				yin = words[1]
				bin_yin = ''
				for y in yin:
					bin_yin += y+'\x00'
				# print bin_yin.encode('hex')
				if self.word_count>0:
					# print len(self.word)
					self.word_offset += struct.pack('i',len(self.word))
					# print self.word_offset.encode('hex')
				self.word_count+=1
				if self.word_count != len_words:
					self.word_length = struct.pack('h',4+len(bin_yin)+2+len(bin_ci))
				else:
					self.word_length = struct.pack('h',len(bin_yin)+2+len(bin_ci))
				# print self.word_length.encode('hex')
				self.word += self.word_start+self.word_length+self.word_local+bin_yin+self.word_delims+bin_ci+self.word_delims
				# print self.word.encode('hex')
			except:
				print line
			
		self.word_count = struct.pack('q',self.word_count)
		# print len(self.word_offset)
		self.data_offset = struct.pack('i',68+len(self.word_offset))
		# print self.data_offset
		self.file_length = struct.pack('i',len(self.file_head+self.data_offset+self.file_length+self.word_count+self.file_date+self.null_data+self.word_offset+self.word))
		return self.file_head+self.data_offset+self.file_length+self.word_count+self.file_date+self.null_data+self.word_offset+self.word
		
	
	def split_src_file(self):
		f = open(self.src_file)
		words = [line.replace('\'','').replace('\t',',').replace('\n','') for line in f]
		f.close()
		return words
		
	
if __name__ == '__main__':
	Lex('ciku.txt','ciku.lex')